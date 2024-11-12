from typing import Dict, List


def prepare_sitelist(lte_nr_pairs: List[Dict[str, str]]) -> str:
    """Prepare a sitelist file from a list of LTE-NR site pairs."""
    sitelist_path = "sitelist.txt"
    key = "LTE site"

    with open(sitelist_path, "w") as sitelist:
        for pair in lte_nr_pairs:
            if key in pair:
                sitelist.write(f"{pair[key]}\n")

    return sitelist_path
