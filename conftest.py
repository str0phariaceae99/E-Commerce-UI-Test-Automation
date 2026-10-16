"""Fixtures globales de pytest."""
import pytest
from utils.driver_factory import get_driver


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecuta Chrome en modo headless (útil para CI).",
    )


@pytest.fixture
def driver(request):
    """Entrega un WebDriver fresco a cada test y lo cierra al final."""
    headless = request.config.getoption("--headless")
    drv = get_driver(headless=headless)
    yield drv
    drv.quit()