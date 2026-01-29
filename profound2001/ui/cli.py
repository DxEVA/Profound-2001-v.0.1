"""
Future CLI/TUI
"""
from profound2001.core.executor import run_system
from profound2001.core.ingestor import Ingestor
from profound2001.core.assimilator import Assimilator

def handle_command(mcp, user_input: str, ctx):
    parts = user_input.strip().split()
    if not parts: return
    cmd = parts[0]
    
    if cmd == "exit":
        return "exit"
    elif cmd == "set" and len(parts) > 2:
        key, val_str = parts[1], parts[2]
        # Auto-convert to int/float if possible
        try:
            if "." in val_str:
                val = float(val_str)
            else:
                val = int(val_str)
        except ValueError:
            val = val_str
        ctx.set(key, val)
        print(f"Set {key} = {val}")
    elif cmd == "run" and len(parts) > 1:
        # Pass existing context
        run_system(mcp, parts[1], context=ctx)
        # Result is already in ctx, output visualized by patterns usually
        # But we can print context state if needed
        # print(f"Context: {ctx}") 
    elif cmd == "ingest" and len(parts) > 2:
        name, filepath = parts[1], parts[2]
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            Ingestor().ingest(name, content)
        except Exception as e:
            print(f"Ingest failed: {e}")
    elif cmd == "assimilate" and len(parts) > 1:
        filepath = parts[1]
        try:
            names = Assimilator().assimilate(filepath)
            print(f"Assimilated: {filepath}")
            # Dynamic Registration
            import importlib
            for name in names:
                # Force reload if it already exists (unlikely in this flow but good practice)
                module_name = f"profound2001.patterns.growth.{name}"
                module = importlib.import_module(module_name)
                importlib.reload(module) 
                
                cls_name = name.capitalize()
                cls = getattr(module, cls_name)
                mcp.register(name, cls)
                print(f"Registered pattern: {name}")

        except Exception as e:
             print(f"Assimilation failed: {e}")
    elif cmd == "bundle" and len(parts) > 2:
        name, output = parts[1], parts[2]
        from profound2001.core.bundler import Bundler
        try:
            Bundler().bundle(name, output, mcp)
        except Exception as e:
            print(f"Bundle failed: {e}")
    elif cmd == "help":
        print("Commands: run <p>, set <k> <v>, ingest <n> <f>, assimilate <f>, bundle <p> <out>, exit")
    else:
        print("Unknown command")

def repl(mcp):
    print("PROFOUND 2001 v0.1")
    from profound2001.runtime.context import Context
    # Persistent context for the session
    session_ctx = Context()
    
    while True:
        try:
            cmd = input("> ")
            if handle_command(mcp, cmd, session_ctx) == "exit":
                break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

