import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    return soup


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


# _______________________________________________Work_with_name_of_artist_______________________________________________

def search_artist(name_artist: str) -> list:
    artists_list = []
    url = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=" + name_artist.replace(" ", "+")
    soup = get_html(url)
    all_info = soup.find('div', class_="component search event-listings events-summary")
    all_artists = all_info.find_all('li', class_="artist")
    for artist in all_artists:
        name = artist.find("strong").text
        link = artist.find('a', class_="thumb").get("href")[9:]
        pic = artist.find('img', class_="profile-pic artist").get("src")
        artists_list.append({"Name": name,
                             "Artist_code": link,
                             "Picture": pic})
    return artists_list


def concert_artist(artist_code: str) -> list:
    concert_list = []
    url = "https://www.songkick.com/artists/" + artist_code
    soup = get_html(url)
    div_inf = soup.find('div', class_="col-8 primary artist-overview")
    try:
        tour_inf = div_inf.find('ul').find('li').text.replace("On tour: ", '')
    except:
        return []
    if tour_inf == "yes":
        calendar = get_html(url + "/calendar")
        concert_event = calendar.find("div", class_="component events-summary upcoming")
        count_concerts = concert_event.find("span", class_="title-copy").text[19:].replace(")", "")
        concert_links = concert_event.find_all("li")
        for concert_link in concert_links:
            link = concert_link.find("a").get("href")
            concert_date = concert_event.find("li", class_="event-listing").get("title")
            concert_place = concert_link.find("strong").text
            concert_hall = concert_link.find("p", class_="secondary-detail").text
            concert_list.append({"Link": link,
                                 "Date": concert_date,
                                 "Concert_hall": concert_hall,
                                 "Place": concert_place})
        return [count_concerts, concert_list]


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
            # conc_city = concert_list.find("p", "location").find("span", class_=None).text
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


if __name__ == "__main__":
    artist_code = "4769598-alison-wonderland"
    #print(concert_artist(artist_code))
    print(search_artist("dua"))
