import os
import argparse
import psycopg2

from src.db.sql import migrations, procedures
from src.db.utils.database import databaseConnect, databaseDisconnect


def migration_down():
    schemas = ["raw", "dbo"]
    conn = databaseConnect()
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
    databaseDisconnect(conn)


def migration_up():
    conn = databaseConnect()
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
    databaseDisconnect(conn)


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
        migration_up()
    elif args.down:
        migration_down()
