import logging
from typing import List, NamedTuple, Tuple

import oracledb
from near_bs.utils import get_env_variable

logger = logging.getLogger(__name__)

LTE_SELECT = """
    SELECT DISTINCT
        SITENAME,
        ROUND(LONGITUDE, 5) AS LONGITUDE,
        ROUND(LATITUDE, 5) AS LATITUDE
    FROM NETWORK_LIVE.LTECELLS2
    WHERE VENDOR = 'Ericsson' AND LONGITUDE IS NOT NULL
    ORDER BY SITENAME ASC
"""

NR_SELECT = """
    SELECT DISTINCT
        SITENAME,
        ROUND(LONGITUDE, 5) AS LONGITUDE,
        ROUND(LATITUDE, 5) AS LATITUDE
    FROM NETWORK_LIVE.NRCELLS
    WHERE VENDOR = 'Ericsson' AND LONGITUDE IS NOT NULL
    ORDER BY SITENAME ASC
"""


db_row = Tuple[str, float, float]


class DbCredentials(NamedTuple):
    """Credentials for Data Base."""

    host: str
    port: int
    service_name: str
    login: str
    password: str


def _get_db_credentials() -> DbCredentials:
    return DbCredentials(
        host=get_env_variable("ATOLL_HOST"),
        port=int(get_env_variable("ATOLL_PORT")),
        service_name=get_env_variable("SERVICE_NAME"),
        login=get_env_variable("ATOLL_LOGIN"),
        password=get_env_variable("ATOLL_PASSWORD"),
    )


def _create_db_connection(credentials: DbCredentials) -> oracledb.Connection:
    dsn = f"{credentials.host}:{credentials.port}/{credentials.service_name}"
    return oracledb.connect(
        user=credentials.login,
        password=credentials.password,
        dsn=dsn,
    )


def select_data() -> Tuple[List[db_row], List[db_row]]:
    """Fetch LTE and NR data from the Network Live database."""
    credentials = _get_db_credentials()
    try:
        with _create_db_connection(credentials) as connection:
            logger.info("Connected to Network Live db")
            with connection.cursor() as cursor:
                cursor.execute(LTE_SELECT)
                lte_data = cursor.fetchall()
                logger.info("Fetched LTE data")

                cursor.execute(NR_SELECT)
                nr_data = cursor.fetchall()
                logger.info("Fetched NR data")
        logger.info("Connection to Network Live db closed")
    except oracledb.DatabaseError:
        logger.error("Database error occured", exc_info=True)
        raise

    return lte_data, nr_data
