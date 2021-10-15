from loguru import logger as dbs_logger
from utils import MyDecorators, MyUtils
from settings import DEBUG_LEVEL
import psycopg2


dbs_logger.add('logs/dbs/logs.log', level=DEBUG_LEVEL)
decorators = MyDecorators(dbs_logger)

class ConnectionPsql:

    def __init__(self, db_credentials):
        self.connection = None
        self.db_credentials = db_credentials

    @decorators.try_except_decorator(full_traceback=True,
                                   max_attempts=3, raise_error=True)
    def __enter__(self) -> dict:
        self.connection = psycopg2.connect(self.db_credentials)
        if self.connection:
            dbs_logger.debug('db connection created')
            return {"connection": self.connection,
                    "cursor": self.connection.cursor()}

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
            dbs_logger.debug('db connection close')


class PsqlManagment:

    def __init__(self, db_credentials:str):
        """
        :param db_credentials: str with psql db credentials
        """
        self.psql_connections = ConnectionPsql(db_credentials)

    def try_execute(self, db_credentials, query):
        try:
            db_credentials["cursor"].execute(query)
            db_credentials["connection"].commit()
        except psycopg2.Error:
            db_credentials["connection"].rollback()
            raise

    @decorators.try_except_decorator(full_traceback=True)
    def execute_psql_query(self, query, db_credentials=None):
        """
        Methods executes sql queries like delete
        records or create table
        :param query: str sql query that should be
        executed
        """
        if db_credentials:
            self.try_execute(db_credentials, query)
        else:
            with self.psql_connections as db_credentials:
                self.try_execute(db_credentials, query)
        return True

    @decorators.try_except_decorator(full_traceback=True)
    def sql_select(self, query):
        """
        Method executes psql select queries
        :param query: str sql query that should be
        executed
        :Return: list of tuples
        """
        with self.psql_connections as db_credentials:
            db_credentials["cursor"].execute(query)
            data_lists = db_credentials["cursor"].fetchall()
        return data_lists

    def mogrify_to_db_list(self, db_credentials, to_db_list):
        signs = '(' + ('%s,' * len(to_db_list[0]))[:-1] + ')'
        args_str = b','.join(db_credentials["cursor"]
                             .mogrify(signs, x) for x in to_db_list)
        args_str = args_str.decode()
        return args_str

    def form_statement(self, table_name,
                       args_str, conflict_st):
        insert_statement = """INSERT INTO %s VALUES """ % table_name
        if conflict_st:
            conflict_statement = conflict_st
        else:
            conflict_statement = """ ON CONFLICT DO NOTHING"""
        return insert_statement + args_str + conflict_statement

    def chunk_writer(self, args_str, table_name,
                     conflict_statement, db_credentials):
        statement_dict = self.form_statement(table_name,
                                             args_str,
                                             conflict_statement)
        written_flag = self.execute_psql_query(statement_dict,
                                               db_credentials=db_credentials)
        return True if written_flag else False

    def empty_data_checker(self, data):
        empty_count = 0
        result_list = []
        for element in data:
            if not element:
                empty_count += 1
            else:
                result_list.append(element)
        if not result_list:
            result_list = None
        return result_list, empty_count

    def write_to_db(self, to_db_list, table_name, chunk_size=1000,
                    bad_case_limit=float("inf"), conflict_statement=None):
        """
        Method writes records to psql database
        :param to_db_list: list of lists
        :param table_name: str name of table
        :Return: None
        """
        bad_case_count = 0
        dbs_logger.info(
                f"Writing to to database started table:: {table_name}"
            )
        with self.psql_connections as db_credentials:
            for chunk in MyUtils.chunk_maker(to_db_list, chunk_size):
                chunk, empty_count = self.empty_data_checker(chunk)
                bad_case_count += empty_count
                written_flag = False
                if bad_case_count >= bad_case_limit:
                    dbs_logger.error('Too many bad case')
                    break
                if chunk:
                    mogrify_chunk = self.mogrify_to_db_list(db_credentials,
                                                            chunk)
                    dbs_logger.debug('Write chunk to db')
                    written_flag = self.chunk_writer(mogrify_chunk, table_name,
                                                     conflict_statement,
                                                     db_credentials)
                    if not written_flag:
                        bad_case_count += len(chunk)
                        continue
                else:
                    dbs_logger.info("Chunk is empty")
            return bad_case_count


if __name__ == "__main__":
    print("dbs_manage module")
