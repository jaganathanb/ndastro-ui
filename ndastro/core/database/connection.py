"""Provide a thread-safe singleton class for managing SQLite database connections.

The DatabaseConnection class ensures proper initialization of the database schema and
provides thread-local connections for safe concurrent access.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from threading import local
from typing import TYPE_CHECKING

from typing_extensions import Self

from config import DB_PATH

if TYPE_CHECKING:
    from collections.abc import Generator


class DatabaseConnection:
    """A thread-safe singleton class for managing SQLite database connections.

    This class ensures that the database is initialized with the proper schema
    and provides thread-local connections for safe concurrent access.

    Methods
    -------
    get_connection() -> Generator[sqlite3.Connection, None]
        Provides a thread-safe connection context manager.
    close_all() -> None
        Closes all thread-local connections.

    """

    _instance = None
    _thread_local = local()

    def __new__(cls) -> Self:
        """Create a new instance of the DatabaseConnection class if it doesn't exist.

        Returns
        -------
        DatabaseConnection
            A singleton instance of the DatabaseConnection class.

        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize()
        return cls._instance

    @classmethod
    def _initialize(cls) -> None:
        """Ensure database exists with proper schema."""
        Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        with cls.get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            # Add any other database initialization here

    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator[sqlite3.Connection, None, None]:
        """Thread-safe connection context manager."""
        if not hasattr(cls._thread_local, "conn"):
            cls._thread_local.conn = sqlite3.connect(
                DB_PATH,
                timeout=20,
                isolation_level=None,
                check_same_thread=False,
            )

        try:
            yield cls._thread_local.conn
        except sqlite3.Error:
            cls._thread_local.conn.rollback()
            raise
        finally:
            pass  # Connection remains open for thread lifetime

    @classmethod
    def close_all(cls) -> None:
        """Close all thread-local connections."""
        if hasattr(cls._thread_local, "conn"):
            cls._thread_local.conn.close()
            del cls._thread_local.conn
