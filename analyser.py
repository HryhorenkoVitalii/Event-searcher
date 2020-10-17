import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


"""
получить ссылку на покупку билета
Если ссылки на покупку билета нет на сайте дает поисковую сылку в гугл
"""


def get_ticket(link_concert):
    url = "https://www.songkick.com/" + link_concert
    soup = get_html(url)
    try:
        ticket_link = soup.find('div', id="tickets").find("a", class_="buy-ticket-link").get("href")
        ticket_vendor = "https://www.songkick.com" + ticket_link
        return ticket_vendor
    except:
        data_search = soup.find("div", class_="date-and-name").text.replace("\n", "").replace(" ", "+")
        name_search = soup.find("h1", class_="h0 summary").text.replace("\n", "").replace(" ", "+")
        location_search = soup.find("div", class_="location").text.replace("\n", "").replace(" ", "+").replace(" ", "+")
        google_link = f"https://www.google.com/search?q={data_search}++{name_search}++{location_search}"
        return google_link


# ________________________________________________Работа по запросу артиста______________________________________________
"""
Ищет артистов по запросу упаковывает в словарь с ключем имя артиста. Возможно несколько артистов.
вход имя (если несколько слов то зменяет " " на "+"
выход { имя артиста [код артиста, ссылка на картинку артиста ]
"""


def search_artist(name_artist):
    artists_dict = {}
    url = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=" + name_artist
    soup = get_html(url)
    all_info = soup.find('div', class_="component search event-listings events-summary")
    all_artists = all_info.find_all('li', class_="artist")
    for artist in all_artists:
        name = artist.find("strong").text
        link = artist.find('a', class_="thumb").get("href")[9:]
        pic = artist.find('img', class_="profile-pic artist").get("src")
        artists_dict[name] = [link, pic]
    return artists_dict


"""
Парсер для страници артиста
Вход: код артиста полученный от бота 
Выход:количество концертов,{сылка на концерт[дата, концертхолл, город_страна(может принимать значение "Canceled" и "POSTPONED")}
"""


def concert_artist(artist_code):
    concert = {}
    url = "https://www.songkick.com/artists/" + artist_code
    soup = get_html(url)
    div_inf = soup.find('div', class_=("col-8 primary artist-overview"))
    try:
        tour_inf = div_inf.find('ul').find('li').text.replace("On tour: ", '')
    except:
        return "Зараз у артиста немає концертiв"
    if tour_inf == "yes":
        calendar = get_html(url + "/calendar")
        conc_event = calendar.find("div", class_="component events-summary upcoming")
        upcoming_conc = conc_event.find("span", class_="title-copy").text[19:].replace(")", "")
        conc_links = conc_event.find_all("li")
        for conc_link in conc_links:
            link = conc_link.find("a").get("href")
            conc_date = conc_event.find("li", class_="event-listing").get("title")
            conc_place = conc_link.find("strong").text
            conc_hall = conc_link.find("p", class_="secondary-detail").text
            concert[link] = [conc_date, conc_hall, conc_place]
        return upcoming_conc, concert


"""
Поиск 50 приведущих концертов 
Вход: код артиста полученный от бота 
выход словарь {дата[место проведения, трана ]}
---работает не всегда, еще допиливаю---
"""


def past_concert(artist_code):
    past_concert = {}
    url = (f"https://www.songkick.com/artists/{artist_code}/gigography")
    soup = get_html(url)
    div_inf = soup.find("div", class_="component events-summary")
    ul_inf = div_inf.find("ul", class_="event-listings")
    concerts = ul_inf.find_all("li")
    count = 0
    for concert in concerts:
        count += 1
        if count % 2 == 0:
            conc_date = concert.get("title")
            try:
                conc_place = concert.find("span", class_="venue-name").find("a").text
            except AttributeError:
                conc_place = None
            #conc_city = concert.find("p", "location").find("span", class_=None).text
            past_concert[conc_date] = [conc_place]
    return past_concert


# _____________________________________Работа по запрсу локации__________________________________________________________
"""
Поиск похожих на ввод пользователя локаций
вход: ввод пользователя 
выход: {локация: часть ссылки + код локации }
"""


def search_location(location):
    location_dict = {}
    url = f"https://www.songkick.com/search?utf8=%E2%9C%93&query={location}"
    soup = get_html(url)
    cities = soup.find_all("li", class_="small-city")
    for city in cities:
        link = city.find("p", class_="summary").find("a").get("href")
        city = city.find("strong").text
        location_dict[city] = link
    return location_dict


"""
Парсер для работы с концертами по локации
вход: код локации, фильтр по дате ("/tonight", "/this weekend", "/this month"), фильтр по жанрам (genre_words)
      если фильрты не применять то парсит все концерты до которых дотянеться.

выход: (количество концертов, {дата(ы)[[Название мероприятия, дополнительное название, место проведение(холл), город,
        ссылка на вероприятие]]}   НЕКОТОРЫЕ ИЗ ЗНАЧЕНИй МОГУТ БЫТЬ ПУСТЫМИ 
"""


def concert_in_location(location_code, filter_by_date=None, filter_by_genre=None):
    concert_location = {}
    # _____________________________________________________нужно скопировать в бот______________________________
    date_words = ["/tonight", "/this weekend", "/this month"]
    genre_words = ["/rock", "/pop", "/Hip-Hop", "/r-and-b", "/indie-alternative", "/electronic", "/country",
                   "/classical", "/metal", "/latin", "/folk", "/jazz", "/funk-soul", "/reggae"]
    # _________________________________________________________________________________________________________
    if filter_by_date in date_words and filter_by_genre in genre_words:
        url = f"https://www.songkick.com{location_code}{filter_by_date}/genre{filter_by_genre}".replace("None", "")
    elif filter_by_date in date_words and filter_by_genre == None:
        url = f"https://www.songkick.com{location_code}{filter_by_date}".replace("None", "")
    elif filter_by_genre in genre_words:
        url = f"https://www.songkick.com{location_code}/genre{filter_by_genre}".replace("None", "")
    else:
        url = f"https://www.songkick.com{location_code}"
    soup = get_html(url)
    currently_ivents = soup.find("p", class_="upcoming-concerts-count").find("b").text
    try:
        all_pages = soup.find("div", class_="pagination").find_all("a")[-2].text
    except AttributeError:
        all_pages = "1"
    for page in range(int(all_pages)):
        print(page + 1)
        url = f"https://www.songkick.com{location_code}?page={(page + 1)}"
        soup = get_html(url)
        div_inf = soup.find("div", id="metro-area-calendar")
        all_ivents = div_inf.find_all("li", class_="event-listings-element")
        for ivent in all_ivents:
            data = ivent.get("title")
            name_1 = ivent.find("strong").text
            try:
                name_2 = ivent.find("span", class_="support").text
            except:
                name_2 = ""
            try:
                ivent_place = ivent.find("a", "venue-link").text
            except:
                ivent_place = ""
            city = ivent.find("span", "city-name").text
            link = ivent.find("a", class_="thumb").get("href")
            if data in concert_location:
                concert_location[data].append([name_1, name_2, ivent_place, city, link])
            else:
                concert_location[data] = [[name_1, name_2, ivent_place, city, link]]
    return currently_ivents, concert_location


def main():
    artist_code = "4769598-alison-wonderland"
    print(concert_artist(artist_code))


if __name__ == "__main__":
    main()
