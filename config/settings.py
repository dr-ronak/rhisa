"""
Configuration settings for RHISA Healthcare Chatbot
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rhisa-healthcare-chatbot-secret-key')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Application settings
    APP_NAME = 'RHISA Healthcare Chatbot'
    APP_VERSION = '1.0.0'
    
    # Supported regions and languages
    SUPPORTED_REGIONS = ['gujarat', 'maharashtra']
    SUPPORTED_LANGUAGES = ['en', 'gu', 'mr']
    DEFAULT_REGION = 'gujarat'
    DEFAULT_LANGUAGE = 'en'
    
    # API settings
    API_VERSION = 'v1'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Rate limiting
    RATE_LIMIT_ENABLED = True
    RATE_LIMIT_DEFAULT = "100 per hour"
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Healthcare domains
    HEALTHCARE_DOMAINS = ['eye_health', 'skin_health']
    
    # Synthetic data settings
    SYNTHETIC_DATA_ENABLED = True
    MAX_SYNTHETIC_PATIENTS = 1000
    
    # Knowledge base settings
    KNOWLEDGE_BASE_ENABLED = True
    MAX_SEARCH_RESULTS = 10
    SEARCH_TIMEOUT = 30  # seconds
    
    # Agent settings
    AGENT_TIMEOUT = 60  # seconds
    MAX_AGENT_RETRIES = 3
    
    # Compliance settings
    COMPLIANCE_CHECK_ENABLED = True
    STRICT_COMPLIANCE_MODE = False
    
    # Multilingual settings
    TRANSLATION_ENABLED = True
    AUTO_DETECT_LANGUAGE = True
    
    # Security settings
    CORS_ENABLED = True
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']
    
    # Performance settings
    CACHE_ENABLED = True
    CACHE_TIMEOUT = 300  # 5 minutes
    
    @classmethod
    def get_region_config(cls, region: str) -> Dict[str, Any]:
        """Get region-specific configuration"""
        region_configs = {
            'gujarat': {
                'name': 'Gujarat',
                'language': 'gu',
                'timezone': 'Asia/Kolkata',
                'health_department': 'Gujarat State Health Department',
                'emergency_number': '108',
                'districts': [
                    'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar',
                    'Gandhinagar', 'Jamnagar', 'Junagadh', 'Anand', 'Bharuch'
                ],
                'primary_health_centers': 1200,
                'population': 60439692
            },
            'maharashtra': {
                'name': 'Maharashtra',
                'language': 'mr',
                'timezone': 'Asia/Kolkata',
                'health_department': 'Maharashtra Health Department',
                'emergency_number': '108',
                'districts': [
                    'Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Aurangabad',
                    'Solapur', 'Thane', 'Kolhapur', 'Sangli', 'Satara'
                ],
                'primary_health_centers': 1800,
                'population': 112374333
            }
        }
        
        return region_configs.get(region.lower(), region_configs['gujarat'])
    
    @classmethod
    def get_language_config(cls, language: str) -> Dict[str, Any]:
        """Get language-specific configuration"""
        language_configs = {
            'en': {
                'name': 'English',
                'code': 'en',
                'direction': 'ltr',
                'font_family': 'Arial, sans-serif'
            },
            'gu': {
                'name': 'ગુજરાતી',
                'code': 'gu',
                'direction': 'ltr',
                'font_family': 'Noto Sans Gujarati, sans-serif'
            },
            'mr': {
                'name': 'मराठी',
                'code': 'mr',
                'direction': 'ltr',
                'font_family': 'Noto Sans Devanagari, sans-serif'
            }
        }
        
        return language_configs.get(language.lower(), language_configs['en'])
    
    @classmethod
    def get_healthcare_domain_config(cls, domain: str) -> Dict[str, Any]:
        """Get healthcare domain-specific configuration"""
        domain_configs = {
            'eye_health': {
                'name': 'Eye Health',
                'icon': '👁️',
                'color': '#2196F3',
                'common_conditions': [
                    'cataract', 'glaucoma', 'diabetic_retinopathy',
                    'conjunctivitis', 'dry_eyes', 'refractive_errors'
                ],
                'specialists': ['ophthalmologist', 'optometrist'],
                'screening_frequency': {
                    'general': 'annual',
                    'diabetic': 'annual',
                    'high_risk': 'bi-annual'
                }
            },
            'skin_health': {
                'name': 'Skin Health',
                'icon': '🧴',
                'color': '#FF9800',
                'common_conditions': [
                    'dermatitis', 'fungal_infections', 'eczema',
                    'psoriasis', 'acne', 'skin_cancer'
                ],
                'specialists': ['dermatologist'],
                'screening_frequency': {
                    'general': 'as_needed',
                    'high_risk': 'annual',
                    'occupational': 'bi-annual'
                }
            }
        }
        
        return domain_configs.get(domain.lower(), {})

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Development-specific settings
    SYNTHETIC_DATA_ENABLED = True
    STRICT_COMPLIANCE_MODE = False
    CACHE_ENABLED = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Production-specific settings
    SYNTHETIC_DATA_ENABLED = True  # Still using synthetic data for privacy
    STRICT_COMPLIANCE_MODE = True
    CACHE_ENABLED = True
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'rhisa-production-secret-key-change-in-production')
    
    # Logging
    LOG_LEVEL = 'INFO'

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Testing-specific settings
    SYNTHETIC_DATA_ENABLED = True
    MAX_SYNTHETIC_PATIENTS = 10
    CACHE_ENABLED = False
    
    # Logging
    LOG_LEVEL = 'DEBUG'

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)