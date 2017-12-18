import os

class Config(object):
    """Parent confirguration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = "chris1234kal"
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:chrisenlarry@localhost:5432/yummys_db'

class DevelopmentConfig(Config):
    """Configurations for Testing, with a separate test database"""
    DEBUG = True

class TestingConfig(Config):
    """Conigurations for Development"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:chrisenlarry@localhost:5432/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging"""
    DEBUG = False

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}