import logging
from typing import NamedTuple

import paramiko
from near_bs.utils import get_env_variable

logger = logging.getLogger(__name__)

REMOTE_PATH = "/home/shared/anpusr/nrAnchor/"
SITELIST = "sitelist.txt"


class EnmSSH(NamedTuple):
    """SSH Credentials for ENM."""

    hostname: str
    username: str
    password: str
    port: int


def _get_enm_credentials() -> EnmSSH:
    return EnmSSH(
        hostname=get_env_variable("ENM_2_IP"),
        username=get_env_variable("ENM_LOGIN"),
        password=get_env_variable("ENM_PASSWORD"),
        port=int(get_env_variable("ENM_PORT")),
    )


def _get_ssh_client(credentials: EnmSSH) -> paramiko.SSHClient:
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(
        hostname=credentials.hostname,
        username=credentials.username,
        password=credentials.password,
        port=credentials.port,
    )
    logger.info("SSH connection to ENM was established")

    return ssh_client


def _upload(ssh_client: paramiko.SSHClient, local_path: str) -> None:
    remote_path = f"{REMOTE_PATH}/{SITELIST}"
    with ssh_client.open_sftp() as sftp:
        sftp.put(local_path, remote_path)
        logger.info("LTE sitelist was uploaded")


def _execute_mobatch(ssh_client: paramiko.SSHClient) -> None:
    mos_path = f"{REMOTE_PATH}/nrAnchor.mos"
    sitelist_path = f"{REMOTE_PATH}/{SITELIST}"
    mobatch_command = (
        f"amosbatch -v username=rbs,password=rbs {sitelist_path} {mos_path}"
    )
    _, stdout, stderr = ssh_client.exec_command(mobatch_command)
    _ = stdout.read() + stderr.read()
    logger.info("mobatch was executed")


def config_nr_anchor(sitelist_path: str) -> None:
    """Configure the NR anchor using the provided path to the sitelist."""
    credentials = _get_enm_credentials()
    with _get_ssh_client(credentials) as ssh_client:
        _upload(ssh_client, sitelist_path)
        _execute_mobatch(ssh_client)