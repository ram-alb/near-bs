import pandas as pd
from geopy.distance import geodesic
from scipy.spatial import KDTree
import math
import logging

logger = logging.getLogger(__name__)


def _find_closest_stations(row, lte_nr_df, lte_nr_tree):
    max_dist = 2
    bs_count = 6
    _, idxs = lte_nr_tree.query([row['latitude'], row['longitude']], k=bs_count)
    closest_bs_list = []
    for idx in idxs:
        bs = lte_nr_df.iloc[idx]
        dist = geodesic((row['latitude'], row['longitude']), (bs['latitude'], bs['longitude'])).km
        if dist <= max_dist:
            closest_bs_list.append(bs)
    return closest_bs_list


def _calc_azimut(point1, point2):
    lat1 = math.radians(point1['latitude'])
    lon1 = math.radians(point1['longitude'])
    lat2 = math.radians(point2['latitude'])
    lon2 = math.radians(point2['longitude'])

    d_lon = lon2 - lon1

    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))

    initial_bearing = math.atan2(x, y)

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def _find_bs_in_sectors(row, closest_bs_list):
    sector1_azimut = 120
    sector2_azimut = 240
    sector3_azimut = 360

    bs_in_sectors = {
        'sector1': None,
        'sector2': None,
        'sector3': None,
    }

    for bs in closest_bs_list:
        azimut = _calc_azimut(row, bs)
        if azimut <= sector1_azimut and bs_in_sectors['sector1'] is None:
            bs_in_sectors['sector1'] = {
                'LTE site': row['site'],
                'neighbor id': bs['site_id'],
                'technology': bs['technology'],
            }
        elif azimut <= sector2_azimut and bs_in_sectors['sector2'] is None:
            bs_in_sectors['sector2'] = {
                'LTE site': row['site'],
                'neighbor id': bs['site_id'],
                'technology': bs['technology'],
            }
        elif azimut <= sector3_azimut and bs_in_sectors['sector3'] is None:
            bs_in_sectors['sector3'] = {
                'LTE site': row['site'],
                'neighbor id': bs['site_id'],
                'technology': bs['technology'],
            }

    return bs_in_sectors


def get_lte_nr_pairs(lte_only_df, lte_nr_df):
    tree = KDTree(lte_nr_df[['latitude', 'longitude']].values)
    lte_nr_pairs = []

    for _, row in lte_only_df.iterrows():
        closest_bs_list = _find_closest_stations(row, lte_nr_df, tree)
        bs_in_sectors = _find_bs_in_sectors(row, closest_bs_list)
        for bs in bs_in_sectors.values():
            if bs is not None and '5G' in bs['technology']:
                lte_nr_pairs.append(bs)
                break

    return lte_nr_pairs
