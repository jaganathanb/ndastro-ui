"""Module to hold the view model."""

from i18n import set as set_i18n_config
from PySide6.QtCore import QObject, Signal

from ndastro.gui.models.ndastro_model import NDAstroModel


class NDAstroViewModel(QObject):
    """ViewModel to hold data & business.

    Args:
        QObject (_type_): _description_

    """

    language_changed = Signal(str)

    def __init__(self, model: NDAstroModel) -> None:
        """Initialize the view model.

        Args:
            model (NDAstroModel): The model

        """
        super().__init__()
        self._model = model  # Reference to the model

    @property
    def title(self) -> str:
        """Title of the main window.

        Returns:
            str: Title

        """
        return self._model.title

    @property
    def locales(self) -> list[tuple[str, str]]:
        """Return language supported.

        Returns:
            list[tuple[str, str]]: List of language name & key

        """
        return self._model.supported_language

    def set_language(self, index: int) -> None:
        """Set language to be used.

        Args:
            index (int): _description_

        """
        lang = self.locales[index]
        set_i18n_config("locale", lang[1])
        self.language_changed.emit(lang[1])
