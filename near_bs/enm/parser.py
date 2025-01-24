import re
from typing import List, Optional, Set

from enmscripting import ElementGroup, TextElement


def _parse_fdn(fdn: str, mo_type: str) -> Optional[str]:
    """Extract a specific MO value from an FDN string based on the provided MO type."""
    mo_patterns = {
        "MeContext": r"MeContext=([^,]+)",
        "SubNetwork": r",SubNetwork=([^,]+)",
    }

    pattern = mo_patterns[mo_type]
    match = re.search(pattern, fdn)
    if match:
        return match.group(1)
    return None


def parse_termpoint_to_gnb(enm_data: List[TextElement]) -> Set[str]:
    """Parse LTE site names from TermPointToGNB ENM data."""
    sites = set()

    for row in enm_data:
        fdn = row.value()
        site = _parse_fdn(fdn, "MeContext")
        if site:
            sites.add(site)

    return sites


def parse_erbs_sites(enm_data: List[ElementGroup]) -> Set[str]:
    """Parse LTE site names if neType is ERBS."""
    sites: Set[str] = set()

    for element_group in enm_data:
        groups = element_group.groups()
        if not groups:
            return sites

        table = groups[0]
        for row in table:
            sitename = row.find_by_label("NodeId")[0].value()
            neType = row.find_by_label("neType")[0].value()
            if neType == "ERBS":
                sites.add(sitename)

    return sites


def find_sites_in_excluded_subnetworks(enm_data: List[TextElement]) -> Set[str]:
    """Find all site names in excluded subnetworks."""
    excluded_subnetworks = ["Astana"]
    sites = set()

    for row in enm_data:
        fdn = row.value()
        site = _parse_fdn(fdn, "MeContext")
        subnetwork = _parse_fdn(fdn, "SubNetwork")

        if subnetwork in excluded_subnetworks:
            sites.add(site)

    return sites
