import yaml

CONFIG_FILE = 'config/config.yaml'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)
