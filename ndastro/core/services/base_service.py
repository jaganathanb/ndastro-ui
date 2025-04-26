"""Base service module.

This module provides the BaseService class, which serves as a foundation
for other service classes by providing common functionality such as logging.
"""

import logging

from ndastro.core.settings.manager import SettingsManager


class BaseService:
    """A base service class providing common functionality for services.

    This class initializes a logger for use in derived service classes.
    """

    def __init__(self, settings_manager: SettingsManager) -> None:
        """Initialize the BaseService with a logger."""
        self.logger = logging.getLogger(
            f"{settings_manager.get('APP', 'name')}_{__name__}.{self.__class__.__name__}",
        )
