import logging
import sys
import re # Import the 're' module for regular expressions
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

def validate_google_drive_url(url: str) -> str:
    """Validate google drive url, returning the folder id


    Args:
        url (str): URL Containing the folder id, you can use the following formats:
            - gd://FOLDER_ID
            - gdrive://FOLDER_ID
            - googledrive://FOLDER_ID
            - gd::FOLDER_ID
            - gdrive::FOLDER_ID
            - googledrive::FOLDER_ID

    Returns:
        str: the folder id

    Raises:
        ValueError: if the url is not valid
    """

    pattern = r"^(?:gd|gdrive|googledrive)(?:://|::)([A-Za-z0-9._-]+)$"
    match = re.match(pattern, url)

    if match:
        folder_id = match.group(1)
        if folder_id: # Ensure FOLDER_ID is not empty
            return folder_id
        else:
            raise ValueError(
                f"Invalid Google Drive URL: '{url}'. FOLDER_ID cannot be empty."
            )
    else:
        raise ValueError(
            f"Invalid Google Drive URL format: '{url}'. "
            "Supported formats: "
            "gd://FOLDER_ID, gdrive://FOLDER_ID, googledrive://FOLDER_ID, "
            "gd::FOLDER_ID, gdrive::FOLDER_ID, googledrive::FOLDER_ID"
        )

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
        help="""Google drive folder id, you can use the following formats:
            - gd://FOLDER_ID
            - gdrive://FOLDER_ID
            - googledrive://FOLDER_ID
            - gd::FOLDER_ID
            - gdrive::FOLDER_ID
            - googledrive::FOLDER_ID""",
    )

    args = parser.parse_args()

    try:
        folder_id = validate_google_drive_url(getattr(args, "remote-url"))
        logger.info(f"Validated Google Drive Folder ID: {folder_id}")
        logger.info(f"Received remote name: {getattr(args, 'remote-name')}")
    except ValueError as e:
        logger.error(e)
        sys.exit(1)