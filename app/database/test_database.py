from sqlalchemy import text

from database.config.database import (
    engine,
    get_db,
)

from database.base.base import (
    Base,
)


print(
    "Base class loaded:",
    Base.__name__,
)


try:

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT 1")
        )

        print(
            "PostgreSQL connection successful:"
        )

        print(
            result.scalar()
        )


    db_generator = get_db()

    db = next(
        db_generator
    )

    print(
        "SQLAlchemy session created successfully."
    )

    db.close()

    print(
        "SQLAlchemy session closed successfully."
    )

except Exception as exc:

    print(
        "Database test failed:"
    )

    print(
        exc
    )
