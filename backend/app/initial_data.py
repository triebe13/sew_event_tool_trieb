import logging

from sqlalchemy.orm import Session

from app.core.db import init_db
from app.database.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """
    Initializes the database session and calls the init_db function to set up the database.

    This function creates a new session using the provided engine and passes it to the init_db function
    to initialize the database with the necessary data.

    Returns:
        None
    """
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    """
    Main function to create initial data for the application.

    This function logs the start of the data creation process, calls the init function to
    initialize the data, and then logs the completion of the data creation process.
    """
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
