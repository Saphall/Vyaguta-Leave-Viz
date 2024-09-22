import os
import sys
import asyncio
import argparse
import psycopg2

from db.src import migrations
from db.src.sql.procedure import extract, transform, load
from db.utils.database import databaseConnect, databaseDisconnect


async def migration_down():
    schemas = ["raw", "std", "dbo"]
    conn = await databaseConnect()
    cur = conn.cursor()
    for schema in schemas:
        cur.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")
    cur.execute(
        """
        SELECT EXISTS (
          SELECT FROM information_schema.tables 
          WHERE table_schema = 'public' 
          AND table_name = '__vyaguta_migrations'
        );
        """
    )
    table_exists = cur.fetchone()[0]
    if table_exists:
        cur.execute("DELETE FROM __vyaguta_migrations WHERE batch <> 0;")
    print("=" * 36)
    print("[-] VyagutaViz Database cleaned!")
    print("=" * 36)
    conn.commit()
    await databaseDisconnect(conn)


async def migration_up():
    conn = await databaseConnect()
    cur = conn.cursor()
    directories = [
        migrations.__path__[0],
        extract.__path__[0],
        transform.__path__[0],
        load.__path__[0],
    ]
    for directory in directories:
        print("=" * 36)
        print(f"Executing scripts for {directory.split('/', maxsplit=-1)[-1]}")
        print("=" * 36)
        for filename in sorted(os.listdir(directory)):
            if directory == migrations.__path__[0]:
                if filename.endswith(".up.sql"):
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
            else:
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
        sys.exit(1)
