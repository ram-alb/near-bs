import csv
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def prepare_sitelist(lte_nr_pairs: List[Dict[str, str]]) -> str:
    """Prepare a sitelist file from a list of LTE-NR site pairs."""
    sitelist_path = "sitelist.txt"
    key = "LTE site"

    with open(sitelist_path, "w") as sitelist:
        for pair in lte_nr_pairs[:5]:
            if key in pair:
                site_name = pair[key]
                if "TEST" in site_name:
                    continue
                sitelist.write(f"{site_name}\n")

    return sitelist_path


def prepare_csv(lte_nr_pairs: List[Dict[str, str]]) -> None:
    with open("lte_nr_pairs.csv", mode="w", newline="") as f:
        fieldnames = lte_nr_pairs[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lte_nr_pairs)
    logger.info("CSV file generated: lte_nr_pairs.csv")
