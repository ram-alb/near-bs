from near_bs.closest_bs import get_lte_nr_pairs
from near_bs.enm.main import main as enm_main
from near_bs.files import prepare_csv, prepare_sitelist
from near_bs.filter import filter_sites_by_enm_data
from near_bs.network_live.main import main as nl_main
from near_bs.ssh import config_nr_anchor


def main(run_mobatch: bool = False):
    """Prepare data for configuration NR Anchor on non co-located LTE site."""
    # get Network Live data
    lte_only_data, uniq_df = nl_main()

    # get ENM data
    enm_data = enm_main()

    # filter sites from network live to exlude sites from ENM
    filtered_data = filter_sites_by_enm_data(lte_only_data, enm_data)

    lte_nr_pairs = get_lte_nr_pairs(filtered_data, uniq_df)

    if run_mobatch:
        sitelist_path = prepare_sitelist(lte_nr_pairs)
        mobatch_reult = config_nr_anchor(sitelist_path)
    else:
        prepare_csv(lte_nr_pairs)
