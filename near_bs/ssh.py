import logging
from typing import NamedTuple

import paramiko
from near_bs.utils import get_env_variable

logger = logging.getLogger(__name__)

REMOTE_PATH = "/home/shared/anpusr/nrAnchor/near_bs_script"
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


def _filter_output(output: str) -> str:
    output_lines = output.split("\n")

    separator_index = None
    separator_count = 0

    for i, line in enumerate(output_lines):
        if set(line) == {"#"}:
            separator_count += 1
            if separator_count == 3:
                separator_index = i
                break

    return (
        "\n".join(output_lines[separator_index + 1:])
        if separator_index is not None
        else output
    )


def _execute_mobatch(ssh_client: paramiko.SSHClient) -> None:
    mos_path = f"{REMOTE_PATH}/nrAnchor.mos"
    sitelist_path = f"{REMOTE_PATH}/{SITELIST}"
    mobatch_command = (
        f"amosbatch -v username=rbs,password=rbs -p 30 {sitelist_path} {mos_path}"
    )

    logger.info("mobatch command execution started.")
    _, stdout, stderr = ssh_client.exec_command(mobatch_command)

    output = stdout.read().decode("utf-8")
    error = stderr.read().decode("utf-8")

    logger.info("mobatch command execution completed.")
    if output:
        filtered_output = _filter_output(output)
        logger.info(f"Command output:\n{filtered_output}")
        return filtered_output
    if error:
        logger.error(f"Command error:\n{error}")
        return error


def config_nr_anchor(sitelist_path: str) -> None:
    """Configure the NR anchor using the provided path to the sitelist."""
    credentials = _get_enm_credentials()
    with _get_ssh_client(credentials) as ssh_client:
        _upload(ssh_client, sitelist_path)
        return _execute_mobatch(ssh_client)
