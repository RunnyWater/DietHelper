import configparser
from pathlib import Path
import socket

class Config:
    _instance = None
    def __new__(cls, config_file='config.cfg'):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls.config_file = config_file
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        self.config = configparser.ConfigParser()
        config_path = Path(self.config_file)
        if not config_path.is_file():
            self._create_default_config()
        self.config.read(self.config_file)


    def _create_default_config(self):
        self.config['database'] = {
            'database_type' : '1',
            'api_key' : 'None',
            'password' : 'None'
        }
        try:
            
            user_name = socket.gethostname()
        except Exception:
            user_name = 'user'
        self.config['user'] = {
            'name': user_name
        }

        self.save()

    def set_database_option(self, option, value):
        section = 'database'
        self.config.set(section, option, value)
        self.save()


    def set_user_name(self, value):
        section = 'user'
        option = 'name'
        self.config.set(section, option, value)
        self.save()


    def save(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get(self, section, option, fallback=None):
        return self.config.get(section, option, fallback=fallback)
    