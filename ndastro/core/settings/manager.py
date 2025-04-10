"""Module to hold SettingsManager class for managing application settings with database storage and change notifications."""

import json
import logging
import sqlite3
import threading
import time

from core.database.connection import DatabaseConnection
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger(__name__)


class SettingsNotifier(QObject):
    """A notifier class to signal when a setting has changed.

    Attributes
    ----------
    setting_changed : Signal
        A signal emitted when a setting changes, providing the key and new value.

    """

    setting_changed = Signal(str, object)  # key, value


class SettingsManager:
    """Manages application settings with database storage and change notifications.

    Attributes
    ----------
    notifier : SettingsNotifier
        An instance of SettingsNotifier to signal setting changes.
    _running : bool
        Indicates whether the change listener thread is running.
    _listener_thread : threading.Thread or None
        The thread object for the change listener.
    _last_change_id : int
        The ID of the last processed setting change.

    Methods
    -------
    get(key: str, default: object = None) -> object
        Retrieve the value associated with a given key.
    set(key: str, value: object) -> None
        Set the value for a given key.
    start_change_listener(interval: float = 0.5) -> None
        Start a background thread to listen for setting changes.
    stop_change_listener() -> None
        Stop the background thread that listens for setting changes.

    """

    def __init__(self) -> None:
        """Initialize the SettingsManager with a notifier, running state, listener thread and last change ID."""
        self.notifier = SettingsNotifier()
        self._running = False
        self._listener_thread = None
        self._last_change_id = 0

    def get(self, key: str, default: object = None) -> object:
        """Retrieve the value associated with the given key from the settings.

        Parameters
        ----------
        key : str
            The key for the setting to retrieve.
        default : object, optional
            The default value to return if the key is not found, by default None.

        Returns
        -------
        object
            The value associated with the key, or the default value if the key is not found.

        """
        with DatabaseConnection.get_connection() as conn:
            cursor = conn.execute(
                "SELECT value FROM settings WHERE key = ?",
                (key,),
            )
            result = cursor.fetchone()
            return json.loads(result[0]) if result else default

    def set(self, key: str, value: object) -> None:
        """Set the value for a given key in the settings.

        Parameters
        ----------
        key : str
            The key for the setting to update or insert.
        value : object
            The value to associate with the key.

        """
        with DatabaseConnection.get_connection() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, json.dumps(value)),
            )
            conn.commit()

    def start_change_listener(self, interval: float = 0.5) -> None:
        """Start a background thread to listen for setting changes.

        Parameters
        ----------
        interval : float, optional
            The interval in seconds between checks for changes, by default 0.5.

        """
        if self._running:
            return

        self._running = True
        self._listener_thread = threading.Thread(
            target=self._listen_for_changes,
            args=(interval,),
            daemon=True,
        )
        self._listener_thread.start()

    def stop_change_listener(self) -> None:
        """Stop the background thread that listens for setting changes."""
        self._running = False
        if self._listener_thread:
            self._listener_thread.join()

    def _listen_for_changes(self, interval: float) -> None:
        while self._running:
            try:
                with DatabaseConnection.get_connection() as conn:
                    cursor = conn.execute(
                        "SELECT id, key FROM setting_changes WHERE id > ? ORDER BY id",
                        (self._last_change_id,),
                    )
                    changes = cursor.fetchall()

                    if changes:
                        self._last_change_id = changes[-1][0]
                        for _, key in changes:
                            value = self.get(key)
                            self.notifier.setting_changed.emit(key, value)
            except (sqlite3.DatabaseError, json.JSONDecodeError) as e:
                logger.exception("Error in settings listener", extra={"error": str(e)})

            time.sleep(interval)
