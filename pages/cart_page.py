"""Page Object del carrito de compras."""
from selenium.webdriver.common.by import By

from utils.self_healing import SelfHealingLocator


class CartPage:
    # --- Locators ---
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING = (By.CSS_SELECTOR, "[data-test='continue-shopping']")

    def __init__(self, driver):
        self.driver = driver
        self.healer = SelfHealingLocator(driver)

    # --- Acciones ---
    def proceed_to_checkout(self) -> "CartPage":
        self.healer.find_element(self.CHECKOUT_BUTTON).click()
        return self

    def continue_shopping(self) -> "CartPage":
        self.healer.find_element(self.CONTINUE_SHOPPING).click()
        return self

    # --- Consultas ---
    def get_item_count(self) -> int:
        return len(self.healer.find_elements(self.CART_ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.healer.find_elements(self.ITEM_NAMES)]