"""
Page Object de la pantalla de Login de saucedemo.com.

Soporta los 6 tipos de usuario de prueba documentados por la plataforma:
- standard_user           → flujo feliz
- locked_out_user         → usuario bloqueado
- problem_user            → UI con bugs intencionales
- performance_glitch_user → latencia artificial
- error_user              → errores aleatorios en acciones
- visual_user             → diferencias visuales / CSS roto
"""
from enum import Enum

from selenium.webdriver.common.by import By

from utils.self_healing import SelfHealingLocator


class UserType(str, Enum):
    """Tipos de usuario disponibles en saucedemo.com."""
    STANDARD = "standard_user"
    LOCKED_OUT = "locked_out_user"
    PROBLEM = "problem_user"
    PERFORMANCE_GLITCH = "performance_glitch_user"
    ERROR = "error_user"
    VISUAL = "visual_user"


class LoginPage:
    URL = "https://www.saucedemo.com/"
    DEFAULT_PASSWORD = "secret_sauce"

    # --- Locators ---
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.healer = SelfHealingLocator(driver)

    # ---------- Navegación ----------

    def load(self) -> "LoginPage":
        self.driver.get(self.URL)
        return self

    # ---------- Acciones ----------

    def login(self, username: str, password: str) -> "LoginPage":
        """Login genérico con credenciales arbitrarias."""
        self.healer.find_element(self.USERNAME).clear()
        self.healer.find_element(self.USERNAME).send_keys(username)
        self.healer.find_element(self.PASSWORD).clear()
        self.healer.find_element(self.PASSWORD).send_keys(password)
        self.healer.find_element(self.LOGIN_BUTTON).click()
        return self

    def login_as(self, user_type: UserType) -> "LoginPage":
        """
        Login de conveniencia usando un tipo de usuario predefinido.

        Ejemplo:
            login_page.login_as(UserType.STANDARD)
            login_page.login_as(UserType.LOCKED_OUT)
        """
        return self.login(user_type.value, self.DEFAULT_PASSWORD)

    # ---------- Consultas ----------

    def get_error_message(self) -> str:
        return self.healer.find_element(self.ERROR_MESSAGE).text

    def is_logged_in(self) -> bool:
        return "inventory.html" in self.driver.current_url

    def is_loaded(self) -> bool:
        return "saucedemo.com" in self.driver.current_url