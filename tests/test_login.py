"""
Tests de Login para saucedemo.com.

Cubre:
- Login exitoso con cada tipo de usuario válido
- Usuario bloqueado
- Credenciales inválidas (password incorrecta, usuario inexistente)
- Validación de campos vacíos
"""
import pytest

from pages.login_page import LoginPage, UserType


@pytest.fixture
def login_page(driver):
    return LoginPage(driver).load()


# ---------- Tests positivos ----------

@pytest.mark.parametrize("user_type", [
    UserType.STANDARD,
    UserType.PROBLEM,
    UserType.PERFORMANCE_GLITCH,
    UserType.ERROR,
    UserType.VISUAL,
])
def test_valid_users_can_login(login_page, user_type):
    login_page.login_as(user_type)
    assert login_page.is_logged_in(), f"{user_type.value} debería poder iniciar sesión"


# ---------- Tests negativos ----------

def test_locked_out_user_is_rejected(login_page):
    login_page.login_as(UserType.LOCKED_OUT)
    assert not login_page.is_logged_in()
    assert "locked out" in login_page.get_error_message().lower()


def test_wrong_password_is_rejected(login_page):
    login_page.login(UserType.STANDARD.value, "wrong_password")
    assert not login_page.is_logged_in()
    assert "do not match" in login_page.get_error_message().lower()


def test_nonexistent_user_is_rejected(login_page):
    login_page.login("ghost_user", "secret_sauce")
    assert not login_page.is_logged_in()
    assert "do not match" in login_page.get_error_message().lower()


def test_empty_username_shows_error(login_page):
    login_page.login("", "secret_sauce")
    assert "username is required" in login_page.get_error_message().lower()


def test_empty_password_shows_error(login_page):
    login_page.login("standard_user", "")
    assert "password is required" in login_page.get_error_message().lower()


def test_both_fields_empty_shows_error(login_page):
    login_page.login("", "")
    assert "username is required" in login_page.get_error_message().lower()


def test_case_sensitive_username(login_page):
    login_page.login("Standard_User", "secret_sauce")
    assert not login_page.is_logged_in()