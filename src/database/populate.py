from sqlalchemy.dialects.postgresql import insert

from src.database.connection import get_context_session
from src.database.models import Auto


async def add_to_db(data: list):
    async with get_context_session() as session:
        for auto in data:
            stmt = insert(Auto).values(
                url=auto["url"],
                title=auto["title"],
                price_usd=auto["price_usd"],
                odometer=auto["odometer"],
                username=auto["username"],
                phone_number=auto["phone_number"],
                image_url=auto["image_url"],
                images_count=auto["images_count"],
                car_number=auto["car_number"],
                car_vin=auto["car_vin"]
            ).on_conflict_do_nothing(index_elements=["url"])

            await session.execute(stmt)
        await session.commit()
