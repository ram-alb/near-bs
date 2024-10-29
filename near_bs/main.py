import csv
import logging

from dotenv import load_dotenv
from near_bs.closest_bs import get_lte_nr_pairs
from near_bs.network_live import select_network_live_data
from near_bs.processing import process_network_live_data
from near_bs.utils import configure_logging

load_dotenv()
logger = logging.getLogger(__name__)


def main():
    """Prepare data for configuration NR Anchor on non co-located LTE site."""
    configure_logging(logging.DEBUG)

    lte_data, nr_data = select_network_live_data()

    lte_only_data, uniq_df = process_network_live_data(lte_data, nr_data)

    logger.info(f"LTE data:\n {lte_only_data.head()}")
    logger.info(f"Merged data:\n {uniq_df.head()}")

    lte_nr_pairs = get_lte_nr_pairs(lte_only_data, uniq_df)
    logger.info(f"LTE_NR pairs:\n {lte_nr_pairs[-10:]}")
    with open("lte_nr_pairs.csv", mode="w", newline="") as f:
        fieldnames = lte_nr_pairs[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lte_nr_pairs)


if __name__ == "__main__":
    main()
