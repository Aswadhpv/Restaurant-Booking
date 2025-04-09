import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Read the Alembic config
config = context.config

# Configure logging from the config file
fileConfig(config.config_file_name)

# Import your model's MetaData object for 'autogenerate'
import sys
import os.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.models import Base  # noqa

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/restaurant_db")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/restaurant_db"),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
