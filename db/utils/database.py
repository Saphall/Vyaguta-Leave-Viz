import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("SERVER", "localhost")
DATABASE = os.getenv("DATABASE", "postgres")
USERNAME = os.getenv("POSTGRES_USER", "sa")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
PORT = os.getenv("DB_PORT", 5432)


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
            port=PORT,
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
