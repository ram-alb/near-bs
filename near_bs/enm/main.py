from typing import Set, Tuple

from near_bs.enm.fetcher import fetch_enm_data
from near_bs.enm.parser import (
    find_sites_in_excluded_subnetworks,
    parse_erbs_sites,
    parse_nr_configured_sites,
)


def main() -> Tuple[Set[str], Set[str], Set[str]]:
    """Get all ENM sites that should be excluded from Nr Anchor configuration."""
    enm_data = fetch_enm_data()

    nr_configured_sites = parse_nr_configured_sites(
        enm_data["GUtraNetwork"], enm_data["GUtranFreqRelation"]
    )
    erbs_sites = parse_erbs_sites(enm_data["MeContext"])
    sites_in_excluded_subnetworks = find_sites_in_excluded_subnetworks(
        enm_data["SubNetwork"]
    )

    return nr_configured_sites, erbs_sites, sites_in_excluded_subnetworks
