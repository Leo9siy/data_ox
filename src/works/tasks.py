import asyncio

from src.parse import main
from src.works.main import app


@app.task
def run_scratch():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    return result
