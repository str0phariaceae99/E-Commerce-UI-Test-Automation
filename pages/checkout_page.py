"""Page Object del flujo de Checkout."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.self_healing import SelfHealingLocator


class CheckoutPage:
    # --- Paso 1: formulario ---
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # --- Paso 2: resumen ---
    FINISH_BUTTON = (By.ID, "finish")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")

    # --- Paso 3: confirmación ---
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    BACK_HOME_BUTTON = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    def __init__(self, driver):
        self.driver = driver
        self.healer = SelfHealingLocator(driver)

    # --- Paso 1 ---
    def fill_customer_info(self, first: str, last: str, zip_code: str) -> "CheckoutPage":
        for locator, value in [
            (self.FIRST_NAME, first),
            (self.LAST_NAME, last),
            (self.POSTAL_CODE, zip_code),
        ]:
            field = self.healer.find_element(locator)
            field.clear()
            if value:
                field.send_keys(value)
        return self

    def click_continue(self) -> "CheckoutPage":
        self.healer.find_element(self.CONTINUE_BUTTON).click()
        return self

    # --- Paso 2 ---
    def click_finish(self) -> "CheckoutPage":
        # Obtenemos el driver desde el healer o el objeto actual (ajusta 'self.driver' según cómo tengas estructurado tu Page Object)
        # Por ejemplo, si tu healer o clase guarda una referencia al driver, úsala aquí:
        driver = getattr(self, 'driver', None) or getattr(self.healer, 'driver', None)
        
        if driver:
            # Espera explícita hasta 10 segundos a que el elemento sea clickeable
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(self.FINISH_BUTTON)
            )

        # Una vez que la espera confirma que existe y está listo, procede con el healer/click
        self.healer.find_element(self.FINISH_BUTTON).click()
        return self
  

    # --- Consultas ---
    def get_error_message(self) -> str:
        return self.healer.find_element(self.ERROR_MESSAGE).text

    def get_confirmation_message(self) -> str:
        return self.healer.find_element(self.COMPLETE_HEADER).text

    def get_total(self) -> str:
        return self.healer.find_element(self.TOTAL).text