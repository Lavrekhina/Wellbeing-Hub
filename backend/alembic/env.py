from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from backend.app.core.config import settings
from backend.app.core.database import Base
from backend.app.models import consent_record, question_response, recommendation, risk_assessment, survey_response

# Alembic Config object, provides access to .ini file values and other context
config = context.config

# Override the SQLAlchemy URL in alembic.ini with runtime settings
config.set_main_option("sqlalchemy.url", settings.database_url)

# Configure Python logging using fileConfig from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate support (all tables registered with Base)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Offline mode generates SQL scripts without connecting to the database.
    Useful for CI/CD pipelines or generating migration scripts manually.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,  # Render values directly in SQL
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Online mode connects to the database and applies migrations directly.
    """
    # Create a SQLAlchemy engine from alembic configuration
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # No connection pooling for migrations
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


# Determine execution mode and run appropriate migration function
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()