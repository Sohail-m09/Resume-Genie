from database.base.base import Base
from database.config.database import engine

# Import all models so SQLAlchemy registers them
# in Base.metadata before create_all() runs.
from database.models import (
    User,
    Resume,
    Job,
    Application,
)


def create_tables() -> None:
    """
    Create all registered SQLAlchemy tables.
    """

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database tables created successfully."
    )


if __name__ == "__main__":
    create_tables()