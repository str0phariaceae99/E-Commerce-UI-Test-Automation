"""Driver factory: crea instancias de WebDriver de forma consistente."""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_driver(headless: bool = False):
    """
    Retorna una instancia de Chrome WebDriver configurada.

    Args:
        headless: Si es True, ejecuta Chrome sin interfaz gráfica (ideal para CI).
    """
    options = Options()

    if headless:
        options.add_argument("--headless=new")

    # --- Opciones generales para CI / estabilidad ---
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    # --- Desactivar password manager, breach detection y autofill ---
    # Esto evita que Chrome muestre el popup "Change your password"
    options.add_argument("--disable-features=PasswordLeakDetection,AutofillServerCommunication")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    # --- Preferencias del perfil (más efectivas que los flags para algunas features) ---
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        "profile.default_content_setting_values.notifications": 2,  # Bloquear notificaciones
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.implicitly_wait(0)
    driver.set_page_load_timeout(20)

    if not headless:
        driver.maximize_window()

    return driver