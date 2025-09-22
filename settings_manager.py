import json
import os
from cryptography.fernet import Fernet
import base64

class SettingsManager:
    def __init__(self):
        self.settings_file = "settings.json"
        self.encrypted_file = "settings.enc"
        self.key_file = "key.key"
        
        # Generate or load encryption key
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
        
        # Load settings
        self.settings = self._load_settings()
    
    def _get_or_create_key(self):
        """Get existing encryption key or create a new one"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _load_settings(self):
        """Load settings from encrypted file"""
        if os.path.exists(self.encrypted_file):
            try:
                with open(self.encrypted_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.cipher.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            except Exception as e:
                print(f"Error loading encrypted settings: {e}")
                return self._get_default_settings()
        elif os.path.exists(self.settings_file):
            # Migrate from unencrypted to encrypted
            try:
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                self._save_settings(settings)
                os.remove(self.settings_file)  # Remove unencrypted file
                return settings
            except Exception as e:
                print(f"Error migrating settings: {e}")
                return self._get_default_settings()
        else:
            return self._get_default_settings()
    
    def _get_default_settings(self):
        """Get default settings"""
        return {
            'last_category': 'US Political News',
            'auto_save_scripts': True,
            'script_save_location': './scripts',
            'max_topics_per_search': 100,
            'search_timeout': 30,
            'enable_notifications': True,
            'dark_mode': True,
            'window_size': '1200x800',
            'last_window_position': None
        }
    
    def _save_settings(self, settings):
        """Save settings to encrypted file"""
        try:
            json_data = json.dumps(settings, indent=2)
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set_setting(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        return self._save_settings(self.settings)
    
    def get_all_settings(self):
        """Get all settings"""
        return self.settings.copy()
    
    def reset_settings(self):
        """Reset all settings to default"""
        self.settings = self._get_default_settings()
        return self._save_settings(self.settings)
    
    def export_settings(self, filename):
        """Export settings to a file (unencrypted for backup)"""
        try:
            # Create a copy without sensitive data
            export_settings = self.settings.copy()
            export_settings['chatgpt_password'] = '***ENCRYPTED***'
            
            with open(filename, 'w') as f:
                json.dump(export_settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, filename):
        """Import settings from a file"""
        try:
            with open(filename, 'r') as f:
                imported_settings = json.load(f)
            
            # Merge with existing settings
            for key, value in imported_settings.items():
                if key != 'chatgpt_password' or value != '***ENCRYPTED***':
                    self.settings[key] = value
            
            return self._save_settings(self.settings)
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def validate_settings(self):
        """Validate application settings"""
        max_topics = self.get_setting('max_topics_per_search', 100)
        
        if not isinstance(max_topics, int) or max_topics < 1 or max_topics > 1000:
            return False, "Max topics must be between 1 and 1000"
        
        return True, "Settings are valid"
    
    def get_script_save_location(self):
        """Get the script save location, creating directory if needed"""
        location = self.get_setting('script_save_location', './scripts')
        
        if not os.path.exists(location):
            try:
                os.makedirs(location)
            except Exception as e:
                print(f"Error creating script directory: {e}")
                location = './scripts'
                if not os.path.exists(location):
                    os.makedirs(location)
        
        return location
    
    def cleanup(self):
        """Clean up temporary files and sensitive data"""
        # Clear any sensitive data from memory
        pass
        
        # Optionally remove key file for extra security
        # if os.path.exists(self.key_file):
        #     os.remove(self.key_file)
