from profound2001.core.mcp import MCP
from profound2001.patterns.builtin.hello_world import HelloWorld
from profound2001.storage.local_store import LocalStore
from profound2001.ui.cli import repl

def main():
    # 1. Init Storage (Future use)
    store = LocalStore()
    _ = store.load()

    # 2. Setup Brain
    mcp = MCP()
    mcp.register("hello_world", HelloWorld)
    

    # Canon
    from profound2001.patterns.canon.math import Add, Sub
    mcp.register("add", Add)
    mcp.register("sub", Sub)

    # 3. Persistence: Load Growth Patterns
    mcp.load_persistence()

    # 3. Enter Loop
    repl(mcp)

if __name__ == "__main__":
    main()

