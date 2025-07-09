import os
from typing import Dict, Any

class AppConfig:
    """Application configuration management"""
    
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment or defaults"""
        return {
            'app': {
                'title': 'Green Smart EcoTourism AI',
                'version': '2.0.0',
                'description': 'Advanced AI for Sustainable Tourism Management',
                'debug': os.getenv('DEBUG', 'false').lower() == 'true'
            },
            'api': {
                'openrouter_base_url': 'https://openrouter.ai/api/v1',
                'default_model': 'qwen/qwq-32b:free',
                'timeout_seconds': 10,
                'max_tokens': 500,
                'temperature': 0.7
            },
            'cache': {
                'ttl_seconds': 300,
                'max_entries': 100
            },
            'ui': {
                'theme_color': '#00ff88',
                'secondary_color': '#66ff99',
                'background_gradient': 'linear-gradient(135deg, #001a0f 0%, #002d1a 25%, #003d25 50%, #002d1a 75%, #001a0f 100%)'
            },
            'features': {
                'ai_chat_enabled': True,
                'image_analysis_enabled': True,
                'scenario_planning_enabled': True,
                'real_time_analytics': True
            }
        }
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation"""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return self.get(f'features.{feature_name}', False)

# Global config instance
app_config = AppConfig()
