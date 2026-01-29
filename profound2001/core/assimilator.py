"""
Library Assimilator
"""
import ast
from profound2001.core.ingestor import Ingestor

class Assimilator:
    def assimilate(self, filepath: str) -> list[str]:
        ingested = []
        with open(filepath, 'r') as f:
            source = f.read()
        for node in ast.parse(source).body:
            if isinstance(node, ast.FunctionDef):
                name = self._ingest_func(node, source)
                ingested.append(name)
        return ingested

    def _ingest_func(self, node, source) -> str:
        # reconstruct body
        func_src = ast.get_source_segment(source, node)
        args = [a.arg for a in node.args.args]
        
        # Wrapper: define func, get args, call, store result
        call_args = ", ".join([f'ctx.get("{a}")' for a in args])
        
        wrapper = f"{func_src}\n"
        wrapper += f"result = {node.name}({call_args})\n"
        wrapper += f"ctx.set('{node.name}', result)\n"
        wrapper += f"print(f'{node.name}: {{result}}')"
        
        Ingestor().ingest(node.name, wrapper)
        return node.name
