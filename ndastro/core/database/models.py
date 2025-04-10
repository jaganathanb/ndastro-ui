"""Define database models for managing application settings.

Include the SettingsModel class, which provides methods to initialize
the database schema for storing settings and tracking changes to those settings.
"""

from .connection import DatabaseConnection


class SettingsModel:
    """Manage application settings in the database.

    Provide methods to initialize the database schema for storing
    settings and tracking changes to those settings.
    """

    @staticmethod
    def initialize_schema() -> None:
        """Create database tables if they don't exist."""
        with DatabaseConnection.get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS setting_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            conn.execute("""
            CREATE TRIGGER IF NOT EXISTS after_settings_update
            AFTER UPDATE ON settings
            FOR EACH ROW
            BEGIN
                INSERT INTO setting_changes (key) VALUES (NEW.key);
            END
            """)
            conn.commit()
