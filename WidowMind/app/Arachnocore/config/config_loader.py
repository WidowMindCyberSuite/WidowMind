import yaml
import platform

CONFIG_FILE = 'config/config.yaml'

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)

    # Detect OS and adjust file_monitor paths dynamically
    if platform.system() == "Windows":
        config['file_monitor']['watch_paths'] = config['file_monitor'].get('windows_paths', [])
    else:
        config['file_monitor']['watch_paths'] = config['file_monitor'].get('linux_paths', [])

    return config

