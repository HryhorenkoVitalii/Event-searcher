from scrapers.abstract_scraper import *


class SongkickScraper(AbstractScraper):

    def __init__(self) -> None:
        super().__init__()

    def get_ticket(self, concert_link: str):
        soup = self.get_soup(concert_link)
        try:
            ticket_link = soup.find('div', id="tickets").find("a", class_="buy-ticket-link").get("href")
            ticket_vendor_url = "https://www.songkick.com" + ticket_link
            return ticket_vendor_url
        except:
            data_search = soup.find("div", class_="date-and-name").text.replace("\n", "").replace(" ", "+")
            name_search = soup.find("h1", class_="h0 summary").text.replace("\n", "").replace(" ", "+")
            location_search = soup.find("div", class_="location").text.replace("\n", "").replace(" ", "+").replace(" ", "+")
            google_link = f"https://www.google.com/search?q={data_search}++{name_search}++{location_search}"
            return google_link


    # __________________________________________Work_with_name_of_artist____________________________________________________

    def get_artist(self, name_artist: str) -> list:
        artists_list = []
        url = "https://www.songkick.com/search?utf8=%E2%9C%93&type=initial&query=" + name_artist.replace(" ", "+")
        soup = self.get_soup(url)
        all_info = soup.find('div', class_="component search event-listings events-summary")
        all_artists = all_info.find_all('li', class_="artist")
        for artist in all_artists:
            name = artist.find("strong").text
            link = artist.find('a', class_="thumb").get("href")[9:]
            picture_endpoint = artist.find('img', class_="profile-pic artist").get("src")
            artists_list.append({"Name": name,
                                 "Artist code": link,
                                 "Picture url": f"http:{picture_endpoint}"})
        return artists_list


    def get_concert(self, artist_code: str) -> dict:
        in_tour = False
        concert_list = []
        count_concerts = 0
        url = f"https://www.songkick.com/artists/{artist_code}/calendar"
        html_request = self.get_request(url)["Data"]
        if html_request.url == url:
            in_tour = True
            soup = BeautifulSoup(html_request.text, 'lxml')
            concert_event = soup.find("div", class_="component events-summary upcoming")
            count_concerts = concert_event.find("span", class_="title-copy").text[19:].replace(")", "")
            concert_links = concert_event.find_all("li")
            for concert_link in concert_links:
                link = concert_link.find("a").get("href")
                concert_date = concert_link.find("time").get("datetime")
                concert_place = concert_link.find("strong").text
                concert_hall = concert_link.find("p", class_="secondary-detail").text
                concert_list.append({"Link": f"https://www.songkick.com{link}",
                                     "Date": concert_date[:10],
                                     "Concert_hall": concert_hall,
                                     "Place": concert_place})
        return {"In tour": in_tour,"Concert list": concert_list, "Concert count": count_concerts}


    def past_concert(self, artist_code: str) -> list:
        past_concert = []
        url = (f"https://www.songkick.com/artists/{artist_code}/gigography")
        soup = self.get_soup(url)
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
                past_concert.append({"Data": conc_date,
                                    "Place": conc_place})
        return past_concert

if __name__ == "__main__":
    print("Soundkick scraper module")