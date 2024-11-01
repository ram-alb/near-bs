import logging
from contextlib import contextmanager
from typing import Generator, List, NamedTuple

import enmscripting  # type: ignore
from enmscripting import ElementGroup, EnmCmdException
from near_bs.utils import get_env_variable

logger = logging.getLogger(__name__)


class EnmCredentials(NamedTuple):
    """Credentials for ENM."""

    server: str
    login: str
    password: str


def _get_enm_credentials(enm: str) -> EnmCredentials:
    return EnmCredentials(
        server=get_env_variable(enm),
        login=get_env_variable("ENM_LOGIN"),
        password=get_env_variable("ENM_PASSWORD"),
    )


@contextmanager
def _enm_session(enm: str) -> Generator:
    """Context manager for opening and closing an ENM session."""
    credentials = _get_enm_credentials(enm)
    try:
        session = enmscripting.open(credentials.server).with_credentials(
            enmscripting.UsernameAndPassword(
                credentials.login,
                credentials.password,
            )
        )
        logger.info(f"Session to ENM {enm} is open.")
        yield session
    except EnmCmdException as e:
        logger.error(f"Failed to open session to ENM {enm}: {e}")
        raise
    finally:
        enmscripting.close(session)
        logger.info(f"Session to ENM {enm} was closed.")


def _cmedit_get(enm: str, command: str) -> ElementGroup:
    with _enm_session(enm) as session:
        cmd = session.command()
        response = cmd.execute(command)

        if not response.is_command_result_available():
            logger.error(f"Response from ENM is not available. Command:\n{command}")
            raise RuntimeError(f"ENM cli command was fail. Command:\n{command}")
        return response.get_output()


def get_gutranetwork_data(enm: str) -> List[ElementGroup]:
    """Get GUtraNetwork data from ENM."""
    gutranetwork_command = (
        "cmedit get * --scopefilter (NetworkElement.neType==RadioNode) "
        "GUtraNetwork.GUtraNetworkId -t"
    )
    return _cmedit_get(enm, gutranetwork_command)
