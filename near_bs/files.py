import csv
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def prepare_sitelist(lte_nr_pairs: List[Dict[str, str]]) -> Optional[str]:
    """Prepare a sitelist file from a list of LTE-NR site pairs."""
    sitelist_path = "sitelist.txt"
    key = "LTE site"
    is_witten = False

    with open(sitelist_path, "w") as sitelist:
        for pair in lte_nr_pairs:
            if key in pair:
                site_name = pair[key]
                if "TEST" in site_name or "GRBS" in site_name:
                    continue
                sitelist.write(f"{site_name}\n")
                is_witten = True

    return sitelist_path if is_witten else None


def prepare_csv(lte_nr_pairs: List[Dict[str, str]]) -> None:
    """Prepare and writes the LTE-NR pairs data to a CSV file."""
    with open("lte_nr_pairs.csv", mode="w", newline="") as f:
        fieldnames = lte_nr_pairs[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(lte_nr_pairs)
    logger.info("CSV file generated: lte_nr_pairs.csv")


def save_text_to_file(text: str, file_path: str) -> str:
    """Save the given output to a text file and returns the path to the file."""
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    return file_path
