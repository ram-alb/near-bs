import os
import pandas as pd

import oracledb

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


ATOLL_HOST = os.getenv("ATOLL_HOST")
ATOLL_PORT = os.getenv("ATOLL_PORT")
SERVICE_NAME = os.getenv("SERVICE_NAME")
ATOLL_LOGIN = os.getenv("ATOLL_LOGIN")
ATOLL_PASSWORD = os.getenv("ATOLL_PASSWORD")


def _select_network_live_data():
    dsn = f"{ATOLL_HOST}:{ATOLL_PORT}/{SERVICE_NAME}"
    with oracledb.connect(
        user=ATOLL_LOGIN, password=ATOLL_PASSWORD, dsn=dsn
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(LTE_SELECT)
            lte_data = cursor.fetchall()

            cursor.execute(NR_SELECT)
            nr_data = cursor.fetchall()
    return lte_data, nr_data


def _add_site_id(selected_data):
    df = pd.DataFrame(selected_data, columns=['site', 'longitude', 'latitude'])
    df['site_id'] = df['site'].str.extract(r'(\d{5})')
    return df


def _remove_duplicates(df):
    df_unique = df.drop_duplicates(subset=['site_id', 'longitude', 'latitude'])
    return df_unique.drop(columns=['site'])


def _add_technology(lte_df, nr_df):
    lte_df['technology'] = lte_df['site_id'].apply(lambda sid: '4G_5G' if sid in nr_df['site_id'].values else '4G')


def _filter_lte_only_sites(lte_df, nr_df):
    return lte_df[~lte_df['site_id'].isin(nr_df['site_id'])]


def get_network_live_data():
    lte_data, nr_data = _select_network_live_data()

    lte_df = _add_site_id(lte_data)
    nr_df = _add_site_id(nr_data)

    lte_only_df = _filter_lte_only_sites(lte_df, nr_df)

    uniq_lte_df = _remove_duplicates(lte_df)
    _add_technology(uniq_lte_df, nr_df)

    return lte_only_df, uniq_lte_df
