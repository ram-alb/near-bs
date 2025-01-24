from typing import Set, Tuple

import pandas as pd


def filter_sites_by_enm_data(
    lte_data: pd.DataFrame,
    enm_data: Tuple[Set[str], Set[str], Set[str]],
) -> pd.DataFrame:
    """Filter LTE-only data by excluding sites present in the ENM data."""
    for enm_sites in enm_data:
        lte_data = lte_data[~lte_data["site"].isin(enm_sites)]
    return lte_data
