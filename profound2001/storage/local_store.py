import json
import os

class LocalStore:
    def __init__(self, filename="profound.json"):
        self.filename = filename

    def load(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def save(self, data: dict):
        with open(self.filename, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=2)
