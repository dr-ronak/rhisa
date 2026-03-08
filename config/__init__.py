"""
RHISA Healthcare Chatbot Configuration Package
"""

from .settings import Config, get_config, DevelopmentConfig, ProductionConfig, TestingConfig

__all__ = ['Config', 'get_config', 'DevelopmentConfig', 'ProductionConfig', 'TestingConfig']