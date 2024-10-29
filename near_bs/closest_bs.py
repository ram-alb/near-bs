import logging
import math
from typing import Any, Dict, List, Optional

import pandas as pd
from geopy.distance import geodesic  # type: ignore
from scipy.spatial import KDTree  # type: ignore

logger = logging.getLogger(__name__)


def _find_closest_stations(
    row: pd.Series, lte_nr_df: pd.DataFrame, lte_nr_tree: KDTree
) -> List[pd.Series]:
    max_dist = 2
    bs_count = 6
    _, idxs = lte_nr_tree.query([row["latitude"], row["longitude"]], k=bs_count)
    closest_bs_list = []
    for idx in idxs:
        bs = lte_nr_df.iloc[idx]
        dist = geodesic(
            (row["latitude"], row["longitude"]), (bs["latitude"], bs["longitude"])
        ).km
        if dist <= max_dist:
            closest_bs_list.append(bs)
        else:
            break
    return closest_bs_list


def _calc_azimut(point1: pd.Series, point2: pd.Series) -> float:
    lat1, lon1 = math.radians(point1["latitude"]), math.radians(point1["longitude"])
    lat2, lon2 = math.radians(point2["latitude"]), math.radians(point2["longitude"])

    delta_lon = lon2 - lon1

    x = math.sin(delta_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (
        math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon)
    )

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def _find_bs_in_sectors(
    row: pd.Series, closest_bs_list: List[pd.Series]
) -> Dict[str, Optional[Dict[str, str]]]:
    sector_limits = {
        "sector1": 120,
        "sector2": 240,
        "sector3": 360,
    }

    bs_in_sectors: Dict[str, Optional[Dict[str, Any]]] = {
        "sector1": None,
        "sector2": None,
        "sector3": None,
    }

    for bs in closest_bs_list:
        azimuth = _calc_azimut(row, bs)
        for sector, limit in sector_limits.items():
            if azimuth <= limit and bs_in_sectors[sector] is None:
                bs_in_sectors[sector] = {
                    "LTE site": row["site"],
                    "neighbor id": bs["site_id"],
                    "technology": bs["technology"],
                }
                break  # Found a base station for this sector, move to next base station

        # Exit early if all sectors are filled
        if all(bs_in_sectors.values()):
            break

    return bs_in_sectors


def get_lte_nr_pairs(
    lte_only_df: pd.DataFrame, lte_nr_df: pd.DataFrame
) -> List[Dict[str, str]]:
    """
    Find pairs of LTE and 5G base stations.

    Find by locating the closest 5G station in defined sectors.
    """
    tree = KDTree(lte_nr_df[["latitude", "longitude"]].values)
    lte_nr_pairs = []

    for _, row in lte_only_df.iterrows():
        closest_bs_list = _find_closest_stations(row, lte_nr_df, tree)
        bs_in_sectors = _find_bs_in_sectors(row, closest_bs_list)
        for bs in bs_in_sectors.values():
            if bs and "5G" in bs["technology"]:
                lte_nr_pairs.append(bs)
                break

    return lte_nr_pairs
