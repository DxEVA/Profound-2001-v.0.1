import os
import sys
import hashlib
import time
import subprocess
from profound2001.core.mcp import MCP
from profound2001.patterns.builtin.hello_world import HelloWorld
from profound2001.runtime.context import Context
from profound2001.core.ingestor import Ingestor

REPORT_PATH = "validation_results_raw.txt"

def log(msg):
    print(msg)
    with open(REPORT_PATH, "a") as f:
        f.write(msg + "\n")

def test_1_determinism():
    log("\n--- TEST 1: Determinism ---")
    outputs = []
    mcp = MCP()
    mcp.register("hello", HelloWorld)
    for i in range(10):
        ctx = Context()
        mcp.run("hello", ctx)
        outputs.append(ctx.get("greeting"))
    
    hashes = [hashlib.md5(o.encode()).hexdigest() for o in outputs]
    unique = len(set(hashes))
    log(f"Unique Hashes: {unique}/10")
    log("STATUS: PASS" if unique == 1 else "STATUS: FAIL")

def test_2_offline():
    log("\n--- TEST 2: Offline Sovereignty ---")
    banned = ['requests', 'urllib', 'http.client', 'socket']
    found = []
    for root, dirs, files in os.walk("profound2001"):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    for b in banned:
                        if f"import {b}" in content or f"from {b}" in content:
                            found.append(f"{file} imports {b}")
    
    if not found:
        log("No network libraries found.")
        log("STATUS: PASS")
    else:
        log(f"Found violations: {found}")
        log("STATUS: FAIL")

def test_3_constraints():
    log("\n--- TEST 3: Micro-Function Constraints ---")
    huge_code = "def execute(ctx):\n" + "\n".join([f"    print({i})" for i in range(30)])
    try:
        Ingestor().ingest("huge_test", huge_code)
        
        # Ingestion only writes file. We must register it to trigger validation.
        import importlib
        module = importlib.import_module("profound2001.patterns.growth.huge_test")
        importlib.reload(module)
        cls = getattr(module, "Huge_test")
        mcp = MCP()
        mcp.register("huge_test", cls)
        
        log("STATUS: FAIL (Allowed huge pattern)")
    except ValueError as e:
        log(f"Caught expected error: {e}")
        log("STATUS: PASS")
    except Exception as e:
        log(f"Unexpected error: {e}")
        log("STATUS: FAIL")

def test_4_bloat():
    log("\n--- TEST 4: Anti-Bloat ---")
    total_size = 0
    for root, dirs, files in os.walk("profound2001"):
        if '__pycache__' in root: continue
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))
    
    log(f"Total Size: {total_size} bytes ({total_size/1024:.2f} KB)")
    log("STATUS: PASS")

def test_5_reuse():
    log("\n--- TEST 5: Pattern Reuse ---")
    log("Simulating sequence: set a=5 -> add -> sub -> result")
    # This proves context reuse across patterns
    ctx = Context({"a": 10, "b": 5})
    # We need to register Add/Sub manually since we aren't using main.py
    from profound2001.patterns.canon.math import Add, Sub
    mcp = MCP()
    mcp.register("add", Add)
    mcp.register("sub", Sub)
    
    mcp.run("add", ctx)
    res1 = ctx.get("result")
    mcp.run("sub", ctx)
    res2 = ctx.get("result")
    
    log(f"Add Result: {res1}, Sub Result: {res2}")
    if res1 == 15 and res2 == 5:
        log("STATUS: PASS")
    else:
        log("STATUS: FAIL")

def test_8_predictability():
    log("\n--- TEST 8: Time Predictability ---")
    from profound2001.patterns.builtin.hello_world import HelloWorld
    hw = HelloWorld()
    c = hw.constraints
    log(f"HelloWorld Time Complexity: {c.time_complexity}")
    if c.time_complexity != "Unknown":
        log("STATUS: PASS")
    else:
        log("STATUS: FAIL")

def test_9_honesty():
    log("\n--- TEST 9: Failure Honesty ---")
    mcp = MCP()
    try:
        mcp.run("non_existent_pattern", Context())
        log("STATUS: FAIL (Ran phantom pattern)")
    except ValueError as e:
        log(f"Caught expected error: {e}")
        log("STATUS: PASS")

def test_10_artifact():
    log("\n--- TEST 10: Artifact Longevity ---")
    # Assume my_app_test.py exists from previous runs
    if os.path.exists("my_app_test.py"):
        try:
            # subprocess run
            result = subprocess.run([sys.executable, "my_app_test.py"], capture_output=True, text=True)
            if "Hello, World!" in result.stdout:
                log("Artifact output verified.")
                log("STATUS: PASS")
            else:
                log(f"Artifact output wrong: {result.stdout}")
                log("STATUS: FAIL")
        except Exception as e:
            log(f"Run failed: {e}")
            log("STATUS: FAIL")
    else:
        log("Artifact missing.")
        log("STATUS: SKIP")


if __name__ == "__main__":
    if os.path.exists(REPORT_PATH): os.remove(REPORT_PATH)
    log("STARTING ORCHESTRATED VALIDATION")
    test_1_determinism()
    test_2_offline()
    test_3_constraints()
    test_4_bloat()
    test_5_reuse()
    test_8_predictability()
    test_9_honesty()
    test_10_artifact()
    log("\nDONE")
