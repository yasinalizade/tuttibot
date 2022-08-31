import aiohttp
import asyncio
import logging


from aiohttp import ClientResponse
from bs4 import BeautifulSoup
# from db_insert import insert
from dotenv import load_dotenv
from fake_useragent import UserAgent
from logging.handlers import RotatingFileHandler


load_dotenv()

logging.basicConfig(
    filename='bot_tutti.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    )

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('bot_tutti.log', maxBytes=500000, backupCount=2)
logger.addHandler(handler)

URL = "https://musopen.org"


async def collect_data(data=""):
    """Collecting data from the web-site. Creating csv-file."""
    if data == "":
        return "There is nothing in database"

    ua = UserAgent()

    headers = {
        'Accept': (
            'text/html,application/xhtml+xml,'
            'application/xml;q=0.9,*/*;q=0.8'
            ),
        'User-Agent': ua.random
    }

    url_for_search = URL + "/ru/music/search/?q=" + "+".join(
        data.lower().split()
    )

    async with aiohttp.ClientSession() as session:
        search_resp: ClientResponse = await session.get(url_for_search,
                                                        headers=headers)
        soup: BeautifulSoup = BeautifulSoup(await search_resp.text(),
                                            "html.parser")
        if soup.find("div", {"class": "noresults text-center"}):
            return "Incorrect request"
        search_address: BeautifulSoup = soup.find('div',
                                                  {"class": "flex-table-row"})
        address = URL + search_address.find("a")["href"]
        response = await session.get(address, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")
        file = soup.find("a", {"id": "sheetmusic-download-button"})["href"]
        piece = soup.find("h1", {"itemprop": "name"}).getText()
        cards = soup.find(
            "div",
            {"class": "col-lg-4 col-md-6 about-piece-info"}).find_all("span")
        instruments = []
        for a in soup.find(
                           "div",
                           {"class": "col-lg-4 col-md-6 about-piece-info"}
        ).find_all("a"):

            if "/ru/music/instrument/" in a["href"]:
                instruments.append(a.getText())
            elif "/ru/music/period/" in a["href"]:
                period = a.getText()

        DATA = []

        for card in cards:
            data = card.getText().strip("\n")
            if (data != "" and data != "Часть / Секция:"
                    and "movements" not in data
                    and 'Become a Patron!' not in data
                    and data not in DATA):
                if "Инструменты:" in DATA:
                    DATA.append("/".join(instruments))
                elif "Инструмент:" in DATA:
                    DATA.append(instruments[0])
                DATA.append(data.strip(", "))
                if "Период:" in DATA:
                    DATA.append(period)

        # insert data in database
        # UNCOMMENT IF YOU RUN DATABASE ON POSTGRESQL
        # diff, time, comp, form, k, instr, per = DATA[1::2]
        # insert(piece, diff, time, comp, form, k, instr, per, file)

        MOVEMENTS = []

        movements = soup.find_all("p", {"class": "mb0"})
        if movements:
            for movement in movements:
                MOVEMENTS.append(movement.getText())
        else:
            MOVEMENTS.append("Movement: --empty--")
    result_list = iter(DATA)
    LIST = "\n".join([el + " " + next(result_list, '') for el in result_list])
    move = "\n".join(MOVEMENTS)
    RESULT = ""
    RESULT += piece + "\n"
    RESULT += LIST + "\n"
    RESULT += move + "\n"
    RESULT += file

    return RESULT


async def main():
    await collect_data()


if __name__ == '__main__':
    # TO UNCOMMENT IF IT DOESN'T WORK ON WINDOWS
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
