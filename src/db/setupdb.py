import os
import asyncio
import argparse
import psycopg2

from src.db.sql import migrations, procedures
from src.db.utils.database import databaseConnect, databaseDisconnect


async def migration_down():
    schemas = ["raw", "dbo"]
    conn = await databaseConnect()
    cur = conn.cursor()
    for schema in schemas:
        cur.execute(
            f""" 
        DROP SCHEMA IF EXISTS {schema} CASCADE;
        """
        )
    print("=" * 36)
    print("[-] VyagutaViz Database cleaned!")
    print("=" * 36)
    conn.commit()
    await databaseDisconnect(conn)


async def migration_up():
    conn = await databaseConnect()
    cur = conn.cursor()
    directories = [migrations.__path__[0], procedures.__path__[0]]
    for directory in directories:
        print("=" * 36)
        print(f"Executing scripts for {directory.split('/', maxsplit = -1)[-1]}")
        print("=" * 36)
        for filename in sorted(os.listdir(directory)):
            if filename.endswith(".sql"):
                with open(
                    os.path.join(directory, filename), "r", encoding="utf-8"
                ) as f:
                    sql_command = f.read()
                    try:
                        cur.execute(sql_command)
                        conn.commit()
                        print(f"  [+] Executed {filename}\n")
                    except psycopg2.Error as e:
                        conn.rollback()
                        print(f"[-] Failed to execute {filename}: ", e)
    await databaseDisconnect(conn)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--up",
        action="store_true",
        help="Run migration_up for Vyaguta Leave Info tables.",
    )
    parser.add_argument(
        "--down",
        action="store_true",
        help="Run migration_down for Vyaguta Leave Info tables.",
    )
    args = parser.parse_args()

    if args.up:
        asyncio.run(migration_up())
    elif args.down:
        asyncio.run(migration_down())
    else:
        print("Please provide a valid argument.")
        parser.print_help()
        exit(1)
