from Parsers import scraper


def name_artist(name: str):
    result = ""
    artist_list = scraper.search_artist(name)
    if len(artist_list) > 1:
        for artist in artist_list:
            result += f"Имя артиста{artist['Name']} "
        return result
    elif len(artist_list) == 1:
        result += f"Имя артиста{artist_list[0]['Name']} "
        return result
    else:
        return "Не нашло артиста"
