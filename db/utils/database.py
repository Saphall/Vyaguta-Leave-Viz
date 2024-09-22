import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("DB_HOST", "localhost")
DATABASE = os.getenv("DB_NAME", "postgres")
USERNAME = os.getenv("DB_USERNAME", "sa")
PASSWORD = os.getenv("DB_PASSWORD")


async def databaseConnect():
    """
    This function helps to connect to database.

    Returns:
    connection: psycopg2 connection object
    """
    try:
        connection = psycopg2.connect(
            user=USERNAME,
            password=PASSWORD,
            host=SERVER,
            port=5432,
            database=DATABASE,
        )
        return connection
    except psycopg2.Error as e:
        raise (e)


async def databaseDisconnect(connection):
    """
    This function helps to disconnect from database.
    """
    try:
        connection.close()
    except psycopg2.Error as e:
        raise (e)
