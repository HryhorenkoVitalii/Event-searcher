import time
import traceback
from datetime import datetime

class TimeIt():
    '''Execute time '''
    def __init__(self,logger, func_name=None, text=None):
        self.logger = logger
        self.text = text
        self.func_name = func_name

    def __enter__(self):
        # self.logger.info("Time :: Start")
        self.time_now = time.time()

    def time_form(self, time):
        result = {"days": 0,
                  "hours": 0,
                  "minutes": 0,
                  "seconds": 0}
        if time > 60:
            result["minutes"] = int(time // 60)
            result["seconds"] = (time) % 60
            if result["minutes"] > 60:
                result["hours"] = int(result["minutes"] // 60)
                result["minutes"] = result["minutes"] % 60
                if result["hours"] > 24:
                    result["days"] = int(result["hours"] // 24)
                    result["hours"] = result["hours"] % 24
        else:
            result["seconds"] = time
        return str(result)

    def form_responce(self):
        format_time = self.time_form(time.time()-self.time_now)
        if self.func_name and not self.text:
            return f"Name: {self.func_name} || Time :: {format_time}"
        elif self.text and not self.func_name:
            return f"Text: {self.text} || Time :: {format_time}"
        else: 
            return f"Name: {self.func_name}, Text: {self.text} || Time :: {format_time}"

    def __exit__(self, exc_type, exc_val, exc_tb):
        responce_text = self.form_responce()
        print(responce_text)
        self.logger.info(responce_text)

def str_to_date_converter(date_str):
    if len(date_str) <= 10:
        data = datetime.strptime(date_str, "%d-%m-%Y")
    else:
        data = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S")
    return data


def chunk_maker(list, number):
    count = 0
    result_list = []
    temp_chunk = []
    for item in list:
        temp_chunk.append(item)
        count += 1
        if count == number:
            result_list.append(temp_chunk)
            temp_chunk = []
            count = 0
    if temp_chunk:
        result_list.append(temp_chunk)
    return result_list

class MyUtils:
    
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def chunk_maker(list, number):
        count = 0
        result_list = []
        temp_chunk = []
        for item in list:
            temp_chunk.append(item)
            count += 1
            if count == number:
                result_list.append(temp_chunk)
                temp_chunk = []
                count = 0
        if temp_chunk:
            result_list.append(temp_chunk)
        return result_list

    def try_except_decorator(self, raise_error=True, full_traceback=False,
                           max_attempts=2, timeout=1, print_stout=False,
                           finally_at_error_case=None):
        """
        :param logger: obj(logger) write
        :param exception: obj(Exception) or exception list
        :param raise_error: bool if True raise error
        :param full_traceback: bool print out traceback
        :param max_attempts: int or None, None = infinite
        :param finally_at_error_case: method to use
        :Return result of wrapper function or Error, or None
        """
        def try_exc(func):
            def function_wrapper(*args, **kwargs):
                attempts = 0
                for number_try in range(max_attempts):
                    attempts += 1
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except Exception:
                        if print_stout:
                            print(f"""Some error occurred with {func.__name__}\n
                                    Retry :: {traceback.format_exc()}""")
                        self.logger.error(
                            f"Some error occurred with {func.__name__}\
                                Retry",
                            exc_info=full_traceback
                        )
                        time.sleep(timeout)
                        if number_try == max_attempts:
                            if print_stout:
                                print(f"""!ERROR :: Can't execute {func.__name__}\n
                                        Retry :: {traceback.format_exc()}""")
                            self.logger.error(
                                f" !ERROR :: Can't execute {func.__name__}",
                                exc_info=full_traceback
                            )
                            if finally_at_error_case:
                                finally_at_error_case()
                            if raise_error is True:
                                raise

            return function_wrapper
        return try_exc

    def time_it_decorator(self, text=None):

        def time_it(func):
            def function_wrapper(*args, **kwargs):
                with TimeIt(logger=self.logger, text=text, lllllfunc_name=func.__name__ ):
                    result = func(*args, **kwargs)
                    print(func.__name__ )
                    return result
            return function_wrapper
        return time_it