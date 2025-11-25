#!/usr/bin/env python3
"""
Deployment configuration loader for EcoGuard
Loads configuration from TOML file or environment variables
"""

import os
import toml

class DeploymentConfig:
    """Configuration manager for EcoGuard deployment"""
    
    def __init__(self, config_file="secrets.toml"):
        """Initialize configuration from TOML file or environment variables"""
        self.config = {}
        
        # Try to load from TOML file first
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config = toml.load(f)
                print(f"Configuration loaded from {config_file}")
            except Exception as e:
                print(f"Error loading {config_file}: {e}")
                self.config = {}
        else:
            print(f"Configuration file {config_file} not found, using environment variables")
        
        # Set environment variables from TOML config if they don't exist
        self._set_env_from_config()
    
    def _set_env_from_config(self):
        """Set environment variables from TOML configuration"""
        # Database configuration
        db_config = self.config.get('database', {})
        self._set_env_if_missing('INFLUXDB_URL', db_config.get('INFLUXDB_URL'))
        self._set_env_if_missing('INFLUXDB_TOKEN', db_config.get('INFLUXDB_TOKEN'))
        self._set_env_if_missing('INFLUXDB_ORG', db_config.get('INFLUXDB_ORG'))
        self._set_env_if_missing('INFLUXDB_BUCKET', db_config.get('INFLUXDB_BUCKET'))
        
        # Communication configuration
        comm_config = self.config.get('communication', {})
        self._set_env_if_missing('TWILIO_ACCOUNT_SID', comm_config.get('TWILIO_ACCOUNT_SID'))
        self._set_env_if_missing('TWILIO_AUTH_TOKEN', comm_config.get('TWILIO_AUTH_TOKEN'))
        self._set_env_if_missing('TWILIO_PHONE_NUMBER', comm_config.get('TWILIO_PHONE_NUMBER'))
        
        # Maps configuration
        maps_config = self.config.get('maps', {})
        self._set_env_if_missing('GOOGLE_MAPS_API_KEY', maps_config.get('GOOGLE_MAPS_API_KEY'))
        
        # Hardware configuration
        hw_config = self.config.get('hardware', {})
        self._set_env_if_missing('RANGER_PHONE_NUMBER', hw_config.get('RANGER_PHONE_NUMBER'))
        
        # Cloud configuration
        cloud_config = self.config.get('cloud', {})
        self._set_env_if_missing('AWS_ACCESS_KEY_ID', cloud_config.get('AWS_ACCESS_KEY_ID'))
        self._set_env_if_missing('AWS_SECRET_ACCESS_KEY', cloud_config.get('AWS_SECRET_ACCESS_KEY'))
        
        # Encryption configuration
        enc_config = self.config.get('encryption', {})
        self._set_env_if_missing('ENCRYPTION_KEY', enc_config.get('ENCRYPTION_KEY'))
        
        # Server configuration
        server_config = self.config.get('server', {})
        self._set_env_if_missing('SECRET_KEY', server_config.get('SECRET_KEY'))
    
    def _set_env_if_missing(self, key, value):
        """Set environment variable if it doesn't already exist"""
        if value and not os.getenv(key):
            os.environ[key] = str(value)
            print(f"Set environment variable: {key}")
    
    def get_database_config(self):
        """Get database configuration"""
        return {
            'url': os.getenv('INFLUXDB_URL'),
            'token': os.getenv('INFLUXDB_TOKEN'),
            'org': os.getenv('INFLUXDB_ORG'),
            'bucket': os.getenv('INFLUXDB_BUCKET')
        }
    
    def get_communication_config(self):
        """Get communication configuration"""
        return {
            'twilio_account_sid': os.getenv('TWILIO_ACCOUNT_SID'),
            'twilio_auth_token': os.getenv('TWILIO_AUTH_TOKEN'),
            'twilio_phone_number': os.getenv('TWILIO_PHONE_NUMBER'),
            'ranger_phone_number': os.getenv('RANGER_PHONE_NUMBER')
        }
    
    def get_maps_config(self):
        """Get maps configuration"""
        return {
            'google_maps_api_key': os.getenv('GOOGLE_MAPS_API_KEY')
        }
    
    def get_cloud_config(self):
        """Get cloud configuration"""
        return {
            'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }
    
    def get_encryption_config(self):
        """Get encryption configuration"""
        return {
            'encryption_key': os.getenv('ENCRYPTION_KEY')
        }
    
    def get_server_config(self):
        """Get server configuration"""
        return {
            'secret_key': os.getenv('SECRET_KEY')
        }

# Initialize configuration
config = DeploymentConfig()

if __name__ == "__main__":
    print("EcoGuard Deployment Configuration")
    print("=" * 40)
    
    # Test configuration loading
    db_config = config.get_database_config()
    print("Database Configuration:")
    for key, value in db_config.items():
        # Mask sensitive values
        if 'token' in key.lower() and value:
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")
    
    comm_config = config.get_communication_config()
    print("\nCommunication Configuration:")
    for key, value in comm_config.items():
        # Mask sensitive values
        if 'token' in key.lower() or 'sid' in key.lower() and value:
            print(f"  {key}: {'*' * len(value) if value else value}")
        else:
            print(f"  {key}: {value}")
    
    maps_config = config.get_maps_config()
    print("\nMaps Configuration:")
    for key, value in maps_config.items():
        # Mask sensitive values
        if 'key' in key.lower() and value:
            print(f"  {key}: {'*' * len(value)}")
        else:
            print(f"  {key}: {value}")