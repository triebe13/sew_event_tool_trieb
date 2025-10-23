import logging

from sqlalchemy import Engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.database.session import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    """
    Initialize the database connection by creating a session and executing a simple query.

    Args:
        db_engine (Engine): The database engine to use for creating the session.
    """
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.execute(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    """
    Main function to initialize the service.
    """
    logger.info("Initializing service")
    init(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
