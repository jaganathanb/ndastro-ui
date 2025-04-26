"""Define the AppContainer, which integrates Core and GUI dependencies.

Integrate core and GUI dependencies of the application using dependency injection.
"""

from dependency_injector import containers, providers

from ndastro.core.core_container import CoreContainer
from ndastro.gui.gui_container import GuiContainer


class AppContainer(containers.DeclarativeContainer):
    """A container for the entire application, combining core and GUI components.

    This class serves as a central point for managing dependencies across the
    application, including both core services and GUI-related components.
    """

    config = providers.Configuration(yaml_files=["config.yaml"])

    core_package = providers.Container(CoreContainer, config=config.core)
    gui_package = providers.Container(GuiContainer, settings_manager=core_package.container.settings_manager)
