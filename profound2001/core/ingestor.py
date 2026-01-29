"""
Logic Ingestor
"""
import os
from profound2001.core.validator import validate_pattern

TEMPLATE = """from profound2001.core.pattern import Pattern, PatternConstraints
from profound2001.runtime.context import Context

class {class_name}(Pattern):
    @property
    def constraints(self) -> PatternConstraints:
        return PatternConstraints(
            time_complexity="Unknown", 
            provenance="Assimilated",
            negative_capabilities=[]
        )

    def execute(self, ctx: Context) -> None:
{body}
"""

class Ingestor:
    def ingest(self, name: str, body: str):
        """Creates a new Pattern file from body logic."""
        class_name = name.capitalize()
        
        # Indent body
        indented_body = "\n".join(["        " + line for line in body.splitlines()])
        
        code = TEMPLATE.format(class_name=class_name, body=indented_body)
        
        # Save first to validate (simplification)
        # Assuming running from parent directory
        path = f"profound2001/patterns/growth/{name}.py"
        with open(path, "w") as f:
            f.write(code)
            
        print(f"Ingested: {path}")
