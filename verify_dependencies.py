#!/usr/bin/env python3
"""
Dependency verification script for Docker build
Checks if all imported modules are in requirements.txt
"""

import os
import re
from pathlib import Path

# Standard library modules (no need to install)
STDLIB_MODULES = {
    'os', 'sys', 'datetime', 'random', 'time', 'json', 'traceback',
    'collections', 'functools', 'itertools', 'typing', 'pathlib',
    'io', 'logging', 're', 'importlib', 'warnings', 'abc'
}

# Module name mappings (import name -> package name)
MODULE_MAPPINGS = {
    'cv2': 'opencv-python-headless',
    'PIL': 'pillow',
    'flask': 'Flask',
    'werkzeug': 'Werkzeug',
    'flask_jwt_extended': 'Flask-JWT-Extended',
    'flask_bcrypt': 'flask-bcrypt',
    'dotenv': 'python-dotenv',
}

def extract_imports(file_path):
    """Extract all import statements from a Python file."""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match: import module
        for match in re.finditer(r'^\s*import\s+(\w+)', content, re.MULTILINE):
            imports.add(match.group(1))
            
        # Match: from module import ...
        for match in re.finditer(r'^\s*from\s+(\w+)', content, re.MULTILINE):
            imports.add(match.group(1))
            
    except Exception as e:
        print(f"[WARN] Error reading {file_path}: {e}")
        
    return imports

def scan_project(root_dir='app'):
    """Scan all Python files in the project."""
    all_imports = set()
    
    for path in Path(root_dir).rglob('*.py'):
        if '__pycache__' in str(path):
            continue
        imports = extract_imports(path)
        all_imports.update(imports)
        
    return all_imports

def load_requirements(req_file='requirements.txt'):
    """Load package names from requirements.txt."""
    packages = set()
    
    try:
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extract package name (before any version specifiers)
                    pkg = re.split(r'[>=<\s]', line)[0].lower()
                    packages.add(pkg)
    except FileNotFoundError:
        print(f"[ERROR] {req_file} not found!")
        return set()
        
    return packages

def verify_dependencies():
    """Main verification function."""
    print("[*] Scanning project for imports...\n")
    
    # Scan project
    imports = scan_project('app')
    
    # Filter out standard library and local app imports
    external_imports = {
        imp for imp in imports 
        if imp not in STDLIB_MODULES and imp != 'app'
    }
    
    # Load requirements
    requirements = load_requirements()
    
    # Check each import
    missing = []
    print("[*] Checking dependencies:\n")
    
    for imp in sorted(external_imports):
        # Map import name to package name
        pkg_name = MODULE_MAPPINGS.get(imp, imp).lower()
        
        if pkg_name in requirements:
            print(f"  [OK] {imp:25} -> {pkg_name:30} [FOUND]")
        else:
            print(f"  [MISS] {imp:25} -> {pkg_name:30} [MISSING]")
            missing.append((imp, pkg_name))
    
    # Summary
    print("\n" + "="*70)
    if missing:
        print(f"\n[FAIL] {len(missing)} missing dependencies!\n")
        print("Add these to requirements.txt:")
        for imp, pkg in missing:
            print(f"  - {pkg}")
        return False
    else:
        print("\n[SUCCESS] All dependencies are in requirements.txt!")
        return True

if __name__ == '__main__':
    success = verify_dependencies()
    exit(0 if success else 1)

