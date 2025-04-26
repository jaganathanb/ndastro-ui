"""Define the GuiContainer class.

Serve as a container for GUI-related models and view models in the NDAstro application.
"""

from dependency_injector import containers, providers

from ndastro.gui.models.dasha import Dasha
from ndastro.gui.models.dasha_detail import DashaDetail
from ndastro.gui.models.kattam import Kattam
from ndastro.gui.models.ndastro_model import NDAstroModel
from ndastro.gui.models.planet_position import PlanetDetail
from ndastro.gui.viewmodels.ndastro_vm import NDAstroViewModel
from ndastro.gui.views.ndastro_ui import NDAstroMainWindow


class GuiContainer(containers.DeclarativeContainer):
    """A container for GUI-related models and view models.

    Attributes
    ----------
    ndastro_model : Factory
        Factory for creating instances of NDAstroModel.
    planet_position_model : Factory
        Factory for creating instances of PlanetDetail.
    kattam_model : Factory
        Factory for creating instances of Kattam.
    dasha_model : Factory
        Factory for creating instances of Dasha.
    dasha_detail_model : Factory
        Factory for creating instances of DashaDetail.
    ndastro_vm : Factory
        Factory for creating instances of NDAstroViewModel with ndastro_model as a dependency.

    """

    core = providers.DependenciesContainer()

    ndastro_model = providers.Factory(NDAstroModel)
    planet_position_model = providers.Factory(PlanetDetail)
    kattam_model = providers.Factory(Kattam)
    dasha_model = providers.Factory(Dasha)
    dasha_detail_model = providers.Factory(DashaDetail)
    settings_manager = core.settings_manager

    ndastro_vm = providers.Factory(
        NDAstroViewModel,
        model=ndastro_model,
        settings_manager=settings_manager,
    )

    ndastro_view = providers.Factory(NDAstroMainWindow, view_model=ndastro_vm, settings_manager=settings_manager)
