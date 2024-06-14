from unittest.mock import patch, MagicMock
import pytest

from psycopg2 import Error as Psycopg2Error
from src.db.utils import database as db


@patch("psycopg2.connect")
def test_databaseConnect(mock_connect):
    mock_connect.return_value = MagicMock()
    connection = db.databaseConnect()
    mock_connect.assert_called_once_with(
        user=db.USERNAME,
        password=db.PASSWORD,
        host=db.SERVER,
        port=5432,
        database=db.DATABASE,
    )
    assert connection == mock_connect.return_value


@patch("psycopg2.connect")
def test_databaseConnect_exception(mock_connect):
    mock_connect.side_effect = Psycopg2Error("Database connection error")
    with pytest.raises(Psycopg2Error, match="Database connection error"):
        db.databaseConnect()
