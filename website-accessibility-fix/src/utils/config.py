"""Configuration management for the website accessibility fix tool."""

import os
import yaml
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """
    Configuration manager for handling application settings.
    
    Supports loading configuration from YAML files and environment variables.
    Environment variables take precedence over file configuration.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file (optional)
        """
        self._config: Dict[str, Any] = {}
        self._config_file = config_file
        
        # Load default configuration
        self._load_defaults()
        
        # Load from file if provided
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_defaults(self) -> None:
        """Load default configuration values."""
        self._config = {
            # Logging configuration
            "logging": {
                "level": "INFO",
                "console_output": True,
                "log_file": "logs/accessibility_fix.log"
            },
            
            # Network diagnostic settings
            "diagnostics": {
                "ping_timeout": 5,
                "port_scan_timeout": 3,
                "traceroute_max_hops": 30,
                "dns_timeout": 5,
                "retry_attempts": 3
            },
            
            # Server analysis settings
            "server": {
                "config_backup_dir": "backups",
                "service_restart_timeout": 30,
                "log_analysis_lines": 1000
            },
            
            # Firewall settings
            "firewall": {
                "backup_rules": True,
                "rule_validation_timeout": 10,
                "web_ports": [80, 443]
            },
            
            # Testing settings
            "testing": {
                "test_timeout": 30,
                "load_test_connections": 10,
                "test_retry_attempts": 3,
                "external_test_sources": []
            },
            
            # Security settings
            "security": {
                "scan_timeout": 60,
                "vulnerability_check": True,
                "security_audit": True
            },
            
            # Monitoring settings
            "monitoring": {
                "check_interval": 300,  # 5 minutes
                "alert_threshold": 3,
                "documentation_dir": "docs"
            }
        }
    
    def _load_from_file(self, config_file: str) -> None:
        """
        Load configuration from YAML file.
        
        Args:
            config_file: Path to configuration file
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
                if file_config:
                    self._merge_config(self._config, file_config)
        except Exception as e:
            print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "WAF_LOG_LEVEL": ("logging", "level"),
            "WAF_LOG_FILE": ("logging", "log_file"),
            "WAF_PING_TIMEOUT": ("diagnostics", "ping_timeout"),
            "WAF_PORT_SCAN_TIMEOUT": ("diagnostics", "port_scan_timeout"),
            "WAF_DNS_TIMEOUT": ("diagnostics", "dns_timeout"),
            "WAF_RETRY_ATTEMPTS": ("diagnostics", "retry_attempts"),
            "WAF_BACKUP_DIR": ("server", "config_backup_dir"),
            "WAF_SERVICE_TIMEOUT": ("server", "service_restart_timeout"),
            "WAF_TEST_TIMEOUT": ("testing", "test_timeout"),
            "WAF_LOAD_TEST_CONNECTIONS": ("testing", "load_test_connections"),
            "WAF_CHECK_INTERVAL": ("monitoring", "check_interval"),
        }
        
        for env_var, (section, key) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert to appropriate type
                if key in ["ping_timeout", "port_scan_timeout", "dns_timeout", 
                          "retry_attempts", "service_restart_timeout", "test_timeout",
                          "load_test_connections", "check_interval"]:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
                
                if section not in self._config:
                    self._config[section] = {}
                self._config[section][key] = value
    
    def _merge_config(self, base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """
        Recursively merge configuration dictionaries.
        
        Args:
            base: Base configuration dictionary
            override: Override configuration dictionary
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found
        
        Returns:
            Configuration value
        """
        return self._config.get(section, {}).get(key, default)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.
        
        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Configuration section name
        
        Returns:
            Configuration section dictionary
        """
        return self._config.get(section, {})
    
    def save_to_file(self, config_file: str) -> None:
        """
        Save current configuration to file.
        
        Args:
            config_file: Path to save configuration file
        """
        # Ensure directory exists
        config_dir = os.path.dirname(config_file)
        if config_dir:
            Path(config_dir).mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, indent=2)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get configuration as dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()