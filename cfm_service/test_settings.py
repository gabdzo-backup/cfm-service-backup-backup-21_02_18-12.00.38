from cfm_service.default_settings import Config


class TestConfig(Config):
    DEBUG = True
    STORAGE = 'memory'
