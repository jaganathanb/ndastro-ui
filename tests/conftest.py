"""Module contains pytest fixtures for the ndastro-ui tests.

Fixtures:
    callattr_ahead_of_alltests(request): A session-scoped fixture that calls a class method `callme`
                                         if it exists, before any tests are run.
    setup(): A session-scoped fixture that sets up internationalization (i18n) configuration
             for the test session.
"""

from pathlib import Path

import pytest
from i18n import set as set_i18n_config

basedir = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session", autouse=True)
def callattr_ahead_of_alltests(request):
    print("callattr_ahead_of_alltests called")
    seen = {None}
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        if cls not in seen:
            if hasattr(cls.obj, "callme"):
                cls.obj.callme()
            seen.add(cls)


@pytest.fixture(scope="session", autouse=True)
def setup() -> None:
    set_i18n_config("file_format", "json")
    set_i18n_config("filename_format", "{namespace}.{locale}.{format}")
    set_i18n_config("load_path", [Path.joinpath(basedir, "ndastro", "locales")])
    set_i18n_config("skip_locale_root_data", value=True)
