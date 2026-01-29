import os

def get_dir_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        # Skip __pycache__
        if '__pycache__' in dirpath: continue
        
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

size = get_dir_size('profound2001')
print(f"PROFOUND Size: {size} bytes")
