def __init__(self, driver, enable_healing: bool = None):
    self.driver = driver
    self.enable_healing = enable_healing if enable_healing is not None else SELF_HEALING_ENABLED