import yaml
from typing import Dict

def read_yaml(filename: str) -> Dict:
    with open(filename, 'r') as f:
        return yaml.safe_load(f)

