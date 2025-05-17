import logging
import sys
from argparse import ArgumentParser

logger = logging.getLogger(__name__)
formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s] %(message)s")

if "app" in __name__:
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.ERROR)

else:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="git-gdrive-remote",
        description="""A helper to use google drive as remote in git""",
    )

    parser.add_argument(
        "remote-name",
        help="Remote name"
    )

    parser.add_argument(
        "remote-url",
        help="Google drive remote name using prefix gd://, gdrive:// or googledrive://",
    )

    args = parser.parse_args()

    logger.info(f"Received remote {args.remote}")

