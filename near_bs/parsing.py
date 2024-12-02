import logging
from typing import Set

from enmscripting import ElementGroup  # type: ignore

logger = logging.getLogger(__name__)


def parse_lte_sites(gutran_network_data: ElementGroup) -> Set[str]:
    """Parse LTE site names from the GUtraNetwork data."""
    sites: Set[str] = set()

    groups = gutran_network_data.groups()
    if not groups:
        logger.warning("No groups found in gutran_network_data.")
        return sites

    table = groups[0]
    for row in table:
        node_ids = row.find_by_label("NodeId")
        if node_ids:
            sites.add(node_ids[0].value())

    return sites


def parse_erbs_sites(netype_data: ElementGroup) -> Set[str]:
    """Parse sites with neType=ERBS from neType data."""
    sites: Set[str] = set()

    groups = netype_data.groups()
    if not groups:
        logger.warning("No groups found in neType data.")
        return sites

    table = groups[0]
    for row in table:
        sitename = row.find_by_label("NodeId")[0].value()
        neType = row.find_by_label("neType")[0].value()
        if neType == "ERBS":
            sites.add(sitename)

    return sites
