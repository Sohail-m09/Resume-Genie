from logging.config import fileConfig
import os

from alembic import context

from dotenv import load_dotenv

from database.base.base import Base

# Import all models so Alembic can detect them.
from database.models import (
    User,
    Resume,
    Job,
    Application,
)


load_dotenv()


config = context.config


database_url = os.getenv(
    "DATABASE_URL"
)

if not database_url:
    raise ValueError(
        "DATABASE_URL is not set in the environment."
    )


if config.config_file_name is not None:
    fileConfig(
        config.config_file_name
    )


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without creating an engine.
    """

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
    )

    with context.begin_transaction():

        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations using a live database connection.
    """

    from sqlalchemy import create_engine

    connectable = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():

            context.run_migrations()


if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()