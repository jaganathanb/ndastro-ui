"""Module to hold the ndastro model."""

from i18n import t


class NDAstroModel:
    """Model for the NDAstro."""

    def __init__(self, locales: list[tuple[str, str]]) -> None:
        """Initialize the model."""
        self.title = t("common.appTitle")
        self.supported_language: list[tuple[str, str]] = locales
