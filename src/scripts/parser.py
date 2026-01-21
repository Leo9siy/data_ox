import asyncio
from pprint import pprint
from urllib.parse import urljoin
import aiohttp

from src.scripts.collector import parse_car_page, get_html, get_car_links


BASEURL = "https://auto.ria.com/"
SEARCH_URL = urljoin(BASEURL, "uk/search/")


async def scrape(
        start_page: int = 1,
        end_page: int = -1,
        concurrency: int = 200
) -> list[dict]:
    sem = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        car_urls = []

        tasks = []
        page = start_page
        while True:
            if end_page != -1 and page > end_page:
                break

            tasks.append(
                asyncio.create_task(process_page(session, page, car_urls))
            )
            page += 1

            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks.clear()

        await asyncio.gather(*tasks)

        car_urls = list(dict.fromkeys(car_urls))

        async def load_and_parse(url: str) -> dict | None:
            try:
                async with sem:
                    html = await get_html(session, url)
                return parse_car_page(html, url)
            except Exception:
                return None

        results = await asyncio.gather(*(load_and_parse(u) for u in car_urls))
        return [r for r in results if r is not None]


async def process_page(session, page, car_urls):
    listing_url = f"{SEARCH_URL}?search_type=2&page={page}"
    listing_html = await get_html(session, listing_url)
    links = get_car_links(BASEURL, listing_html)

    if links:
        car_urls.extend(links)
        print(f"Processed page {page}")


if __name__ == "__main__":
    data = asyncio.run(scrape(1, 5, concurrency=30))
    pprint(data)
