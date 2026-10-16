"""
Tests del flujo de Checkout.
"""
import pytest

from pages.login_page import LoginPage, UserType
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def checkout_form(driver):
    """Deja el test posicionado en el formulario del Paso 1 del checkout."""
    LoginPage(driver).load().login_as(UserType.STANDARD)
    InventoryPage(driver).add_first_item_to_cart().go_to_cart()
    CartPage(driver).proceed_to_checkout()
    return CheckoutPage(driver)


# ---------- Happy path ----------

def test_complete_checkout_flow(checkout_form):
    checkout_form.fill_customer_info("Juan", "Pérez", "110111")
    checkout_form.click_continue()
    checkout_form.click_finish()
    assert "Thank you for your order" in checkout_form.get_confirmation_message()


def test_checkout_summary_shows_total(checkout_form):
    checkout_form.fill_customer_info("Juan", "Pérez", "110111")
    checkout_form.click_continue()
    total = checkout_form.get_total()
    assert "$" in total


# ---------- Validación de formulario ----------

def test_checkout_without_first_name_shows_error(checkout_form):
    checkout_form.fill_customer_info("", "Pérez", "110111")
    checkout_form.click_continue()
    assert "first name is required" in checkout_form.get_error_message().lower()


def test_checkout_without_last_name_shows_error(checkout_form):
    checkout_form.fill_customer_info("Juan", "", "110111")
    checkout_form.click_continue()
    assert "last name is required" in checkout_form.get_error_message().lower()


def test_checkout_without_postal_code_shows_error(checkout_form):
    checkout_form.fill_customer_info("Juan", "Pérez", "")
    checkout_form.click_continue()
    assert "postal code is required" in checkout_form.get_error_message().lower()


def test_checkout_with_all_fields_empty_shows_first_error(checkout_form):
    checkout_form.fill_customer_info("", "", "")
    checkout_form.click_continue()
    assert "first name is required" in checkout_form.get_error_message().lower()


# ---------- Documentar comportamiento de problem_user ----------

@pytest.mark.xfail(reason="problem_user tiene bugs intencionales en el inventario")
def test_problem_user_checkout(driver):
    LoginPage(driver).load().login_as(UserType.PROBLEM)
    InventoryPage(driver).add_first_item_to_cart().go_to_cart()
    CartPage(driver).proceed_to_checkout()
    checkout = CheckoutPage(driver)
    checkout.fill_customer_info("Test", "User", "12345")
    checkout.click_continue()
    checkout.click_finish()
    assert "Thank you for your order" in checkout.get_confirmation_message()