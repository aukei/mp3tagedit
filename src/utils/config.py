"""
Configuration module for the MP3 Tag Editor application
"""
import os
import json
from pathlib import Path

CONFIG_DIR = os.path.join(str(Path.home()), ".mp3tagedit")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "last_directory": "",
    "sample_size": 10,
    "recursive_search": True,
    "window_width": 800,
    "window_height": 600,
    "auto_process": False
}

def ensure_config_dir():
    """Ensure the configuration directory exists"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_config():
    """
    Load the configuration from the config file
    
    Returns:
        dict: Configuration dictionary
    """
    ensure_config_dir()
    
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        # Ensure all default keys are present
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                config[key] = value
        
        return config
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """
    Save the configuration to the config file
    
    Args:
        config (dict): Configuration dictionary
    """
    ensure_config_dir()
    
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving configuration: {e}")

def get_config_value(key, default=None):
    """
    Get a configuration value
    
    Args:
        key (str): Configuration key
        default: Default value if key is not found
        
    Returns:
        Configuration value
    """
    config = load_config()
    return config.get(key, default)

def set_config_value(key, value):
    """
    Set a configuration value
    
    Args:
        key (str): Configuration key
        value: Configuration value
    """
    config = load_config()
    config[key] = value
    save_config(config)