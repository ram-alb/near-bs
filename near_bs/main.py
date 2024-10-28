from dotenv import load_dotenv

load_dotenv()

import logging
import csv

from near_bs.network_live import get_network_live_data
from near_bs.closest_bs import get_lte_nr_pairs

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s:%(name)s:%(levelname)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    lte_only_data, merged_data  = get_network_live_data()

    logger.info(f"LTE data:\n {lte_only_data.head()}")
    logger.info(f"Merged data:\n {merged_data.head()}")

    lte_nr_pairs = get_lte_nr_pairs(lte_only_data, merged_data)
    logger.info(f'LTE_NR pairs:\n {lte_nr_pairs[-10:]}')
    with open('lte_nr_pairs.csv', mode='w', newline='') as f:
        fieldnames = lte_nr_pairs[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lte_nr_pairs)


if __name__ == "__main__":
    main()