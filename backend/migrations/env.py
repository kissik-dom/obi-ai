"""Alembic schema migration environment targeting Kingdom AI OS SQLAlchemy 2.0 metadata."""

from __future__ import annotations

from alembic import context
from backend.core.stores import Base, RELATIONAL_ENGINE

target_metadata = Base.metadata


def run_migrations_online() -> None:
    with RELATIONAL_ENGINE.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    context.configure(url=str(RELATIONAL_ENGINE.url), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations_online()
