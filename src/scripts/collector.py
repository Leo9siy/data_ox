import re
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}


async def get_html(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, headers=HEADERS) as r:
        r.raise_for_status()
        return await r.text()


def get_car_links(base_url: str, listing_html: str) -> list[str]:
    soup = BeautifulSoup(listing_html, "lxml")
    links = []
    for a in soup.select("a.link.product-card"):
        href = a.get("href")
        if href:
            links.append(urljoin(base_url, href))
    return links


def parse_car_page(car_html: str, url: str) -> dict:
    parser = BeautifulSoup(car_html, "lxml")

    title = parser.select_one("div#sideTitleTitle > span")
    title = title.text if title else ""

    price_usd = parser.select_one("div#sidePrice > strong")
    price_usd = int("".join(re.findall(r'\d', price_usd.text)))\
        if price_usd else ""

    odometer = parser.select_one("div#basicInfoTableMainInfo0 > span")
    odometer = int(odometer.text.split(" ")[0]) * 1000 if odometer else 0

    username = parser.select_one("div#sellerInfoUserName > span")
    username = username.text if username else "Not found"

    phone_number = parser.select_one("div#sellerInfo button span.action")
    phone_number = "".join(re.findall(r'\d', phone_number.text)) \
        if parser.select_one("div#sellerInfo button span.action") else "0"

    image_url = parser.select_one("span.picture img")
    image_url = image_url.get("data-src") if image_url else ""

    images_count = parser.select_one(
        "div#photoSlider > span > span:nth-child(2)"
    )
    images_count = int(images_count.text) if images_count else 0

    car_number = parser.select_one("div.car-number.ua")
    car_number = car_number.text if car_number else ""

    car_vin = parser.select_one("div.badge-template > span > span")
    car_vin = car_vin.text if car_vin else ""

    return {
        "url": url,
        "title": title,
        "price_usd": price_usd,
        "odometer": odometer,

        "username": username,
        "phone_number": int("38" + phone_number),
        "image_url": image_url,
        "images_count": images_count,

        "car_number": car_number,
        "car_vin": car_vin
    }
