import logging
import os

from near_bs.files import save_text_to_file
from send_mail import send_email

logger = logging.getLogger(__name__)


def send_mobatch_result_by_mail(mobatch_result: str) -> None:
    """Send the result of the mobatch execution as an email attachment."""
    attachment_path = save_text_to_file(mobatch_result, "mobatch_result.txt")

    to = os.getenv("TO")

    subject = "NR Anchor Configuration Results"
    message = (
        "Good day,\n\n"
        "Please find the NR Anchor configuration results attached.\n\n"
        "Best regards,\n"
        "Your Automation Script\n"
        "Made by NDS-RNPOU-RNSD Team"
    )

    logger.info("Preparing to send mobatch results via email.")

    send_email(
        to,
        subject,
        message,
        filepaths=[attachment_path],
    )

    logger.info("Mobatch results have been successfully sent via email.")
