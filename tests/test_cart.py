"""
Tests del carrito de compras y ordenamiento de productos.
"""
import pytest

from pages.login_page import LoginPage, UserType
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.fixture
def inventory_page(driver):
    LoginPage(driver).load().login_as(UserType.STANDARD)
    return InventoryPage(driver)


# ---------- Agregar al carrito ----------

def test_add_single_item_updates_badge(inventory_page):
    inventory_page.add_first_item_to_cart()
    assert inventory_page.get_cart_badge_count() == 1


def test_add_all_items_updates_badge(inventory_page):
    inventory_page.add_all_items_to_cart()
    assert inventory_page.get_cart_badge_count() == 6


def test_badge_not_visible_when_cart_is_empty(inventory_page):
    assert inventory_page.get_cart_badge_count() == 0


# ---------- Remover del carrito ----------

def test_remove_item_updates_badge(inventory_page):
    inventory_page.add_all_items_to_cart()
    inventory_page.remove_first_item_from_cart()
    assert inventory_page.get_cart_badge_count() == 5


# ---------- Vista del carrito ----------

def test_cart_shows_added_items(driver, inventory_page):
    inventory_page.add_first_item_to_cart()
    inventory_page.go_to_cart()
    cart = CartPage(driver)
    assert cart.get_item_count() == 1


def test_cart_is_empty_initially(driver, inventory_page):
    inventory_page.go_to_cart()
    cart = CartPage(driver)
    assert cart.get_item_count() == 0


# ---------- Ordenamiento ----------

def test_sort_by_name_ascending(inventory_page):
    inventory_page.sort_by("az")
    names = inventory_page.get_product_names()
    assert names == sorted(names)


def test_sort_by_name_descending(inventory_page):
    inventory_page.sort_by("za")
    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True)


def test_sort_by_price_low_to_high(inventory_page):
    inventory_page.sort_by("lohi")
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices)


def test_sort_by_price_high_to_low(inventory_page):
    inventory_page.sort_by("hilo")
    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices, reverse=True)