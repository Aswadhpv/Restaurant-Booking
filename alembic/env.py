import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Read the Alembic config
config = context.config

# Configure logging from the config file
fileConfig(config.config_file_name)

# Insert project root into sys.path for module discovery
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import the Base and ensure your models are imported
from app.models import Base
import app.models.table         # Import table model module
import app.models.reservation   # Import reservation model module

target_metadata = Base.metadata

def run_migrations_offline():
    url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/restaurant_db")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True,
        dialect_opts={"paramstyle": "named"}
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
