"""Module to hold ND Astro app."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication


class NDAstro(QApplication):
    """Main app instance for ND Astro.

    Args:
        QApplication (_type_): The application

    """

    language_changed = Signal(str)
