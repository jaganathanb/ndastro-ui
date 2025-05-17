"""Abstract base dialog class for dialog controls in the ndastro UI."""

from abc import ABC, abstractmethod

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QWidget


class BaseDialogMeta(type(ABC), type(QWidget)):
    """Metaclass for combining ABC and QWidget metaclasses in dialog controls."""


class BaseDialogContent(ABC, QWidget, metaclass=BaseDialogMeta):
    """Abstract base class for dialog controls."""

    @property
    @abstractmethod
    def close_dialog(self) -> SignalInstance:
        """Abstract signal property for close signal."""
