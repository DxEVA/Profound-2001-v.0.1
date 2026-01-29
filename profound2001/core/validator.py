"""
Enforces constraints
"""
import ast
import inspect
import textwrap

def validate_pattern(pattern_cls):
    """
    Validates a pattern class against strict constraints.
    Max 22 lines per method.
    """
    source = textwrap.dedent(inspect.getsource(pattern_cls))
    tree = ast.parse(source)
    
    
    BLACKLIST = {
        'os', 'subprocess', 'shutil', 'sys', 'glob', 'socket', 'requests', 'urllib', 'http', 'pickle'
    }
    method_count = 0
    has_constraints = False

    for node in ast.walk(tree):
        # 1. Security Check
        if isinstance(node, ast.Import):
            for alias in node.names:
                base_module = alias.name.split('.')[0]
                if base_module in BLACKLIST:
                    raise ValueError(f"Security Violation: Import '{alias.name}' is forbidden.")
        
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                base_module = node.module.split('.')[0]
                if base_module in BLACKLIST:
                    raise ValueError(f"Security Violation: From-import '{node.module}' is forbidden.")

        # 2 & 3. Method Constraints & Metadata
        elif isinstance(node, ast.FunctionDef):
            # Check Metadata
            if node.name == 'constraints':
                has_constraints = True
            
            # Check Micro-Function Law
            method_count += 1
            length = node.end_lineno - node.lineno + 1
            if length > 22:
                msg = f"Method '{node.name}' exceeds 22 lines ({length})."
                raise ValueError(msg)
                
    if method_count > 4:
         raise ValueError(f"Pattern exceeds 4 methods ({method_count}). strict limit.")

    if not has_constraints:
        raise ValueError("Pattern must explicitly define 'constraints' property.")
         
    return True

