from typing import List, Tuple

import pandas as pd
from near_bs.network_live import db_row


def _prepare_dataframe(selected_data: List[db_row]) -> pd.DataFrame:
    df = pd.DataFrame(selected_data, columns=["site", "longitude", "latitude"])
    df["site_id"] = df["site"].str.extract(r"(\d{5})", expand=False).fillna(0)
    return df


def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    df_unique = df.drop_duplicates(subset=["site_id", "longitude", "latitude"])
    return df_unique.drop(columns=["site"])


def _add_technology(lte_df: pd.DataFrame, nr_df: pd.DataFrame) -> None:
    lte_df["technology"] = (
        lte_df["site_id"].isin(nr_df["site_id"]).map({True: "4G_5G", False: "4G"})
    )


def _filter_lte_only_sites(lte_df: pd.DataFrame, nr_df: pd.DataFrame) -> pd.DataFrame:
    return lte_df[~lte_df["site_id"].isin(nr_df["site_id"])]


def process_network_live_data(
    lte_data: List[db_row], nr_data: List[db_row]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Process LTE and NR data.

    Prepare DataFrames with filtered LTE-only sites and unique LTE
    sites with technology information.
    """
    lte_df = _prepare_dataframe(lte_data)
    nr_df = _prepare_dataframe(nr_data)

    lte_only_df = _filter_lte_only_sites(lte_df, nr_df)

    uniq_lte_df = _remove_duplicates(lte_df)
    _add_technology(uniq_lte_df, nr_df)

    return lte_only_df, uniq_lte_df
