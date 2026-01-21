import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

from src.config import settings


script_dir = Path(__file__).resolve().parent


async def make_dump():
    backups_dir = script_dir.parent / "dumps"
    backups_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = backups_dir / (f"backup_"
                                 f"{settings.POSTGRES_NAME}_{timestamp}.dump")

    command = [
        "pg_dump",
        "-h", settings.POSTGRES_HOST,
        "-p", str(settings.POSTGRES_PORT),
        "-U", settings.POSTGRES_USER,
        "-d", settings.POSTGRES_NAME,
        "-F", "c",
        "-f", str(backup_file)
    ]

    env = os.environ.copy()
    env["PGPASSWORD"] = settings.POSTGRES_PASSWORD

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await process.communicate()  # for errors

        if process.returncode == 0:
            print(f"Dump data '{settings.POSTGRES_NAME}' successful,"
                  f" made file: {backup_file}")
        else:
            print(f"Error while dump: {stderr.decode('utf-8')}")
            sys.exit(1)

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")
