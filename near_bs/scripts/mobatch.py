import logging

from dotenv import load_dotenv
from near_bs.main import main
from near_bs.utils import configure_logging

load_dotenv()

configure_logging(logging.INFO)


def mobatch():
    main(run_mobatch=True)
