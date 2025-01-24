from collections import defaultdict
from typing import Dict, List, Union

from enm_cli import cmedit_get_many
from enmscripting import ElementGroup, TextElement

cli_commads = {
    "TermPointToGNB": "cmedit get *RBS* TermPointToGNB",
    "MeContext": "cmedit get *RBS_* MeContext.neType -t",
    "SubNetwork": "cmedit get *RBS_* MeContext",
}


ENM_SERVERS = ("ENM_2", "ENM_4")


def fetch_enm_data() -> Dict[str, Union[List[ElementGroup], List[TextElement]]]:
    """Fetch all ENM data according to cli_commadns."""
    mo_with_table_output = [
        mo for mo, command in cli_commads.items() if "-t" in command
    ]
    enm_data = defaultdict(list)

    for enm in ENM_SERVERS:
        enm_results = cmedit_get_many(enm, cli_commads)
        for mo, enm_result in enm_results.items():
            if mo in mo_with_table_output:
                enm_data[mo].append(enm_result)
            else:
                enm_data[mo].extend(enm_result)

    return enm_data
