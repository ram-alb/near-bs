from typing import Tuple

import pandas as pd
from near_bs.network_live.fetcher import select_data
from near_bs.network_live.processing import process_data


def main() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main function to select and process network live data.

    Fetches LTE and NR data from the database, processes it, and returns:
    - A DataFrame with LTE-only sites.
    - A DataFrame with unique LTE sites enriched with technology information.
    """
    # select network live data
    lte_data, nr_data = select_data()

    # process network live data
    lte_only_data, uniq_df = process_data(lte_data, nr_data)

    return lte_only_data, uniq_df
