"""
Deterministic execution
"""
from profound2001.core.mcp import MCP
from profound2001.runtime.context import Context

def run_system(mcp: MCP, pattern, data: dict = None, context: Context = None):
    """
    Entry point to run the system deterministically.
    """
    if context is None:
        context = Context(data)
    elif data:
        # If both provided, merge data into existing context
        for k, v in data.items():
            context.set(k, v)
            
    mcp.run(pattern, context)
    return context

