from typing import Set, Tuple

from near_bs.enm.fetcher import fetch_enm_data
from near_bs.enm.parser import (
    find_sites_in_excluded_subnetworks,
    parse_erbs_sites,
    parse_sites_from_fdn,
)


def main() -> Tuple[Set[str], Set[str], Set[str]]:
    """Get all ENM sites that should be excluded from Nr Anchor configuration."""
    enm_data = fetch_enm_data()

    sites_with_gutran_freq_relation = parse_sites_from_fdn(enm_data["GUtranFreqRelation"])
    erbs_sites = parse_erbs_sites(enm_data["MeContext"])
    sites_in_excluded_subnetworks = find_sites_in_excluded_subnetworks(
        enm_data["SubNetwork"]
    )

    return sites_with_gutran_freq_relation, erbs_sites, sites_in_excluded_subnetworks
