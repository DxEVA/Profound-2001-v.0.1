"""
Micro Control Plane (brain)
"""
from typing import Dict, Type
from profound2001.core.pattern import Pattern
from profound2001.runtime.context import Context
from profound2001.core.validator import validate_pattern

class MCP:
    """
    Micro Control Plane.
    The central brain that manages and executes patterns.
    """
    def __init__(self):
        self._registry: Dict[str, Type[Pattern]] = {}

    def register(self, name: str, pattern_cls: Type[Pattern]):
        validate_pattern(pattern_cls)
        self._registry[name] = pattern_cls

    def load_persistence(self, directory: str = "profound2001/patterns/growth"):
        """Loads persistent patterns from the growth directory."""
        import os
        import importlib
        if os.path.exists(directory):
            print(f"Loading persistent patterns from {directory}...")
            for f in os.listdir(directory):
                if f.endswith(".py") and f != "__init__.py":
                    name = f[:-3]
                    try:
                        # Convert path to module dotted path
                        # deeply nested path logic is tricky if directory varies, 
                        # but we stick to standard layout "profound2001.patterns.growth"
                        module_path = directory.replace("/", ".").replace("\\", ".")
                        module = importlib.import_module(f"{module_path}.{name}")
                        # Assume class name is Capitalized(name)
                        cls_name = name.capitalize()
                        cls = getattr(module, cls_name)
                        self.register(name, cls)
                        print(f"  + Loaded: {name}")
                    except Exception as e:
                        print(f"  ! Failed to load {name}: {e}")

    def run(self, pattern_name: str, context: Context):
        if pattern_name not in self._registry:
            raise ValueError(f"Pattern '{pattern_name}' not found.")
        
        pattern_cls = self._registry[pattern_name]
        instance = pattern_cls()
        # Composition Bridge (Test 13)
        context._mcp = self
        instance.execute(context)
