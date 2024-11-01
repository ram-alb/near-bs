import csv
import logging

from dotenv import load_dotenv
from near_bs.closest_bs import get_lte_nr_pairs
from near_bs.enm import get_gutranetwork_data
from near_bs.network_live import select_network_live_data
from near_bs.parsing import parse_lte_sites
from near_bs.processing import process_network_live_data
from near_bs.utils import configure_logging

load_dotenv()
logger = logging.getLogger(__name__)


def main():
    """Prepare data for configuration NR Anchor on non co-located LTE site."""
    configure_logging(logging.DEBUG)

    # select network live data
    lte_data, nr_data = select_network_live_data()

    # get ENM data
    enm2_gutrannetwork_data = get_gutranetwork_data("ENM_2")
    enm4_gutrannetwork_data = get_gutranetwork_data("ENM_4")

    # process network live data
    lte_only_data, uniq_df = process_network_live_data(lte_data, nr_data)

    # parse ENM data
    enm2_sites = parse_lte_sites(enm2_gutrannetwork_data)
    enm4_sites = parse_lte_sites(enm4_gutrannetwork_data)
    enm_sites = enm2_sites | enm4_sites
    logger.info(f"ENM sites:\n {enm_sites}")

    # filter sites from network live to exlude sites from ENM
    filtered_sites = lte_only_data[~lte_only_data["site"].isin(enm_sites)]

    logger.info(f"LTE data:\n {filtered_sites.head()}")
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
