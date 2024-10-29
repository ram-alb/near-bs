import logging
import os
from typing import Union


def get_env_variable(var_name: str) -> str:
    """Return the value of an environment variable or raises an exception."""
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Environment variable '{var_name}' is not defined.")
    return value


def configure_logging(level: Union[str, int]) -> None:
    """Configure the logging settings with a specified logging level and format."""
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=(
            "[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d "
            "%(levelname)s %(message)s"
        ),
    )
