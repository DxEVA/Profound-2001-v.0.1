import os
import sys
import time
import importlib
import shutil
from profound2001.core.mcp import MCP
from profound2001.runtime.context import Context
from profound2001.core.ingestor import Ingestor
from profound2001.core.validator import validate_pattern

REPORT_PATH = "validation_results_advanced.txt"

def log(msg):
    print(msg)
    with open(REPORT_PATH, "a") as f:
        f.write(msg + "\n")

def test_12_persistence():
    log("\n--- TEST 12: Cross-Session Persistence ---")
    # Simulate session 1: create file
    p_path = "profound2001/patterns/growth/persist_test.py"
    if not os.path.exists(p_path):
        Ingestor().ingest("persist_test", "print('I exist')")
    
    # Simulate session 2: Load MCP fresh
    mcp = MCP()
    # Now explicitly call load logic
    mcp.load_persistence()
    
    # Check if 'persist_test' is available? 
    try:
        mcp.run("persist_test", Context())
        log("STATUS: PASS (Persistence works)")
    except ValueError:
        log("STATUS: FAIL (Pattern not auto-loaded)")

def test_13_composition():
    log("\n--- TEST 13: Pattern Composition ---")
    try:
        # We need to manually register the composition test pattern first (since auto-load might miss it if we didn't restart)
        # But wait, Persistence test 12 runs before this. Main.py runs persist load.
        # But this script runs MCP directly. Code above uses MCP() directly.
        # So we must register 'add' and 'composition_test' manually here.
        mcp = MCP()
        from profound2001.patterns.canon.math import Add
        mcp.register("add", Add)
        
        # Load comp test
        import importlib
        module = importlib.import_module("profound2001.patterns.growth.composition_test")
        importlib.reload(module)
        cls = getattr(module, "Composition_test")
        mcp.register("composition_test", cls)
        
        ctx = Context()
        ctx.set("val", 7) # Expects val -> sets a=7, b=7 -> add -> 14
        mcp.run("composition_test", ctx)
        
        res = ctx.get("result")
        log(f"Composition Result: {res}")
        if res == 14:
             log("STATUS: PASS")
        else:
             log("STATUS: FAIL")
    except Exception as e:
        log(f"STATUS: FAIL (Error: {e})")

def test_14_clarification():
    log("\n--- TEST 14: Clarification Loop ---")
    log("STATUS: NOT_IMPLEMENTED")

def test_15_extraction():
    log("\n--- TEST 15: Library Extraction ---")
    # We use external_lib.py which we tested before
    lib_path = "profound2001/external_lib.py"
    if os.path.exists(lib_path):
        # We assume assimilation worked in Test 3/10 or we re-run it
        # Check generated file size
        gen_path = "profound2001/patterns/growth/multiply.py"
        if os.path.exists(gen_path):
            size = os.path.getsize(gen_path)
            log(f"Generated Pattern Size: {size} bytes")
            # Check for numpy imports?
            with open(gen_path, 'r') as f:
                content = f.read()
            if "import numpy" not in content:
                log("No external dependencies found.")
                log("STATUS: PASS (Extraction successful)")
            else:
                log("STATUS: FAIL (Dependencies remain)")
        else:
            log("STATUS: FAIL (Pattern not generated)")
    else:
        log("STATUS: ERROR (Library missing)")

def test_16_edge_cases():
    log("\n--- TEST 16: Edge Case Handling ---")
    mcp = MCP()
    try:
        mcp.run("", Context())
        log("STATUS: FAIL (Accepted empty string)")
    except ValueError:
        log("STATUS: PASS (Rejected empty string)")

def test_17_multifile():
    log("\n--- TEST 17: Multi-File Projects ---")
    log("STATUS: NOT_IMPLEMENTED")

def test_18_git():
    log("\n--- TEST 18: Version Control Integration ---")
    if os.path.exists(".git"):
        log("Git repo detected.")
        log("STATUS: PARTIAL (Repo exists, but auto-commit not implemented)")
    else:
        log("STATUS: NOT_IMPLEMENTED")

def test_19_benchmarks():
    log("\n--- TEST 19: Performance Benchmarks ---")
    from profound2001.patterns.builtin.hello_world import HelloWorld
    mcp = MCP()
    mcp.register("hw", HelloWorld)
    start = time.time()
    mcp.run("hw", Context())
    end = time.time()
    duration = (end - start) * 1000
    log(f"Simple Pattern Run: {duration:.2f} ms")
    if duration < 500:
        log("STATUS: PASS (<500ms)")
    else:
        log("STATUS: FAIL (Too slow)")

def test_20_growth():
    log("\n--- TEST 20: User Library Growth ---")
    count = 0
    size = 0
    growth_dir = "profound2001/patterns/growth"
    if os.path.exists(growth_dir):
        for f in os.listdir(growth_dir):
            if f.endswith(".py"):
                count += 1
                size += os.path.getsize(os.path.join(growth_dir, f))
    
    log(f"Pattern Count: {count}")
    log(f"Library Size: {size} bytes")
    if count > 0 and size < 100000: # 100KB
        log("STATUS: PASS")
    else:
        log("STATUS: FAIL/EMPTY")

def test_21_security():
    log("\n--- TEST 21: Security/Safety ---")
    # Try to ingest dangerous code
    dangerous_code = "import os\nos.system('echo dangerous')"
    try:
        Ingestor().ingest("dangerous", dangerous_code)
        # If it ingested, we check if validator stopped it? 
        # Ingestor just writes. Assimilator uses Ingestor.
        # Validator is run on register.
        # Let's see if we can register it.
        import importlib
        module = importlib.import_module("profound2001.patterns.growth.dangerous")
        importlib.reload(module) # Force reload
        cls = getattr(module, "Dangerous")
        
        # Manually validate (MCP does this)
        validate_pattern(cls)
        
        # If we got here, it passed validation
        log("STATUS: FAIL (Allowed 'import os')")
    except ValueError as e:
        log(f"Caught validation error: {e}")
        log("STATUS: PASS (Blocked)")
    except ImportError:
        log("STATUS: ERROR (Import failed)")
    except Exception as e:
        log(f"STATUS: FAIL (Allowed? Error: {e})")

def test_22_documentation():
    log("\n--- TEST 22: Documentation Generation ---")
    # Test Bundler.generate_readme
    from profound2001.core.bundler import Bundler
    b = Bundler()
    b.generate_readme("TestArtifact", ".")
    if os.path.exists("README.md"):
        with open("README.md") as f:
            c = f.read()
        if "TestArtifact" in c and "Usage" in c:
            log("STATUS: PASS")
        else:
            log("STATUS: FAIL (Invalid Content)")
        os.remove("README.md")
    else:
        log("STATUS: FAIL (File not created)")

if __name__ == "__main__":
    if os.path.exists(REPORT_PATH): os.remove(REPORT_PATH)
    log("STARTING ADVANCED VALIDATION")
    test_12_persistence()
    test_13_composition()
    test_14_clarification()
    test_15_extraction()
    test_16_edge_cases()
    test_17_multifile()
    test_18_git()
    test_19_benchmarks()
    test_20_growth()
    test_21_security()
    test_22_documentation()
    log("\nDONE")
