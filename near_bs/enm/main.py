from typing import Set, Tuple

from near_bs.enm.fetcher import fetch_enm_data
from near_bs.enm.parser import (
    find_sites_in_excluded_subnetworks,
    parse_erbs_sites,
    parse_termpoint_to_gnb,
)


def main() -> Tuple[Set[str], Set[str], Set[str]]:
    """Get all ENM sites that should be excluded from Nr Anchor configuration."""
    enm_data = fetch_enm_data()

    sites_with_termpoints = parse_termpoint_to_gnb(enm_data["TermPointToGNB"])
    erbs_sites = parse_erbs_sites(enm_data["MeContext"])
    sites_in_excluded_subnetworks = find_sites_in_excluded_subnetworks(
        enm_data["SubNetwork"]
    )

    return sites_with_termpoints, erbs_sites, sites_in_excluded_subnetworks
