"""Define the CoreContainer class, a dependency injection container.

It manages core services in the ndastro application and provides
singleton instances of services such as NdAstroService, KattamService,
DashaService, and the SettingsManager.
"""

import logging
import logging.config
import os
from collections.abc import Generator
from concurrent.futures import ThreadPoolExecutor

from dependency_injector import containers, providers

from ndastro.core.services.dasha_service import DashaService
from ndastro.core.services.kattam_service import KattamService
from ndastro.core.services.ndastro_service import NdAstroService
from ndastro.core.settings.manager import SettingsManager


def _init_thread_pool(max_workers: int) -> Generator[ThreadPoolExecutor, None, None]:
    """Initialize a thread pool executor.

    Parameters
    ----------
    max_workers : int
        The maximum number of threads that can be used by the thread pool.

    Yields
    ------
    ThreadPoolExecutor
        A thread pool executor instance.

    Ensures proper shutdown of the thread pool after use.

    """
    thread_pool = ThreadPoolExecutor(max_workers=max_workers)
    yield thread_pool
    thread_pool.shutdown(wait=True)


class CoreContainer(containers.DeclarativeContainer):
    """Manage core services using a dependency injection container.

    Provide singleton instances of various services such as NdAstroService,
    KattamService, and DashaService, as well as the SettingsManager.
    """

    config = providers.Configuration()

    thread_pool = providers.Resource(
        _init_thread_pool,
        max_workers=os.cpu_count() or 1,
    )

    logging = providers.Resource(
        logging.config.dictConfig,
        config=config.logging,
    )

    settings_manager = providers.Singleton(SettingsManager, "settings.ini")

    ndastro_service = providers.Singleton(NdAstroService, settings_manager=settings_manager)
    kattam_service = providers.Singleton(KattamService, settings_manager=settings_manager)
    dasha_service = providers.Singleton(DashaService, settings_manager=settings_manager)
