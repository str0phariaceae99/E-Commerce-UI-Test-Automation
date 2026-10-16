"""Page Object del catálogo de productos (Inventory)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from utils.self_healing import SelfHealingLocator


class InventoryPage:
    # --- Locators basados en data-test (más estables) ---
    INVENTORY_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    def __init__(self, driver):
        self.driver = driver
        self.healer = SelfHealingLocator(driver)

    # --- Acciones ---
    def add_first_item_to_cart(self) -> "InventoryPage":
        self.healer.find_elements(self.ADD_TO_CART_BUTTONS)[0].click()
        return self

    def add_all_items_to_cart(self) -> "InventoryPage":
        for btn in self.healer.find_elements(self.ADD_TO_CART_BUTTONS):
            btn.click()
        return self

    def remove_first_item_from_cart(self) -> "InventoryPage":
        buttons = self.healer.find_elements(self.REMOVE_BUTTONS)
        if buttons:
            buttons[0].click()
        return self

    def sort_by(self, option_value: str) -> "InventoryPage":
        """option_value: 'az', 'za', 'lohi', 'hilo'."""
        Select(self.healer.find_element(self.SORT_DROPDOWN)).select_by_value(option_value)
        return self

    def go_to_cart(self) -> "InventoryPage":
        self.healer.find_element(self.CART_LINK).click()
        return self

    # --- Consultas ---
    def get_cart_badge_count(self) -> int:
        try:
            return int(self.healer.find_element(self.CART_BADGE).text)
        except Exception:
            return 0

    def get_product_names(self) -> list[str]:
        return [el.text for el in self.healer.find_elements(self.ITEM_NAMES)]

    def get_product_prices(self) -> list[float]:
        return [
            float(el.text.replace("$", ""))
            for el in self.healer.find_elements(self.ITEM_PRICES)
        ]