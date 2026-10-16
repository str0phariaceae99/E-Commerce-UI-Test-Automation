"""
Self-Healing Locator Utility.

Cuando un selector falla, consulta a un LLM local (Ollama) para que analice
el DOM actual y proponga un selector CSS alternativo. Registra cada evento
de auto-reparación en un reporte JSON para auditoría.
"""
import json
import os
import re
from datetime import datetime, timezone

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# ----- Configuración -----
SELF_HEALING_ENABLED = os.getenv("SELF_HEALING_ENABLED", "true").lower() == "true"
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
REPORT_PATH = os.path.join("reports", "healing_events.json")
REQUEST_TIMEOUT = 30


class SelfHealingLocator:
    """Wrapper alrededor de WebDriver que auto-repara selectores rotos."""

    def __init__(self, driver, enable_healing: bool = True):
        self.driver = driver
        self.enable_healing = enable_healing
        self.healing_events = []
        os.makedirs("reports", exist_ok=True)

    # ---------- API pública ----------

    def find_element(self, locator: tuple):
        """Busca un elemento; si falla, intenta auto-reparar el selector."""
        by, value = locator
        try:
            return self.driver.find_element(by, value)
        except NoSuchElementException:
            if not self.enable_healing:
                raise
            print(f"[SelfHealing] Locator falló: {by}={value}. Consultando al LLM...")
            healed_selector = self._ask_ollama_for_selector(by, value)

            if not healed_selector:
                print("[SelfHealing] El LLM no propuso un selector válido.")
                raise

            try:
                element = self.driver.find_element(By.CSS_SELECTOR, healed_selector)
                self._log_healing_event(by, value, healed_selector)
                print(f"[SelfHealing] ✅ Selector reparado: {healed_selector}")
                return element
            except NoSuchElementException:
                print(f"[SelfHealing] ❌ El selector sugerido tampoco funcionó: {healed_selector}")
                raise

    def find_elements(self, locator: tuple):
        """Versión plural; sin auto-reparación para no enredar la lógica."""
        by, value = locator
        return self.driver.find_elements(by, value)

    # ---------- Internos ----------

    def _ask_ollama_for_selector(self, by: str, value: str) -> str | None:
        """Pide al LLM local un selector CSS alternativo."""
        # Tomamos solo una porción del DOM para no saturar el prompt
        dom_snippet = self.driver.page_source[:8000]

        prompt = (
            "You are an expert Selenium automation engineer.\n"
            f"A test failed because the element with {by}=\"{value}\" was not found.\n"
            "Analyze the following HTML and return ONLY the best CSS selector "
            "for that element. Do not include explanations, quotes, or markdown.\n\n"
            f"HTML:\n{dom_snippet}\n\n"
            "CSS selector:"
        )

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            raw = response.json().get("response", "").strip()

            # Limpiar: nos quedamos solo con la primera línea limpia
            selector = raw.splitlines()[0].strip().strip('`"\'')
            # Descartar respuestas que claramente no son selectores CSS
            if not selector or len(selector) > 200 or " " in selector[:1]:
                return None
            # Validación mínima: que sea un selector CSS plausible
            if not re.match(r"^[#.\[\w\-_:>* ]+$", selector):
                return None
            return selector

        except requests.exceptions.RequestException as e:
            print(f"[SelfHealing] Error al comunicarse con Ollama: {e}")
            return None

    def _log_healing_event(self, by: str, original: str, healed: str) -> None:
        """Registra el evento de auto-reparación en el reporte JSON."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "original_locator": f"{by}={original}",
            "healed_locator": healed,
            "url": self.driver.current_url,
        }
        self.healing_events.append(event)

        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(self.healing_events, f, indent=2, ensure_ascii=False)