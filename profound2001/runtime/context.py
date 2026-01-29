"""
Explicit state passing
"""

class Context:
    """
    Mutable state container for Pattern execution.
    Acts as the single source of truth during a pipeline run.
    """
    def __init__(self, initial_data: dict = None):
        self._store = initial_data or {}

    def get(self, key, default=None):
        return self._store.get(key, default)

    def set(self, key, value):
        self._store[key] = value

    def __repr__(self):
        return f"<Context keys={list(self._store.keys())}>"

