#!/usr/bin/env python3
"""
Script to clear Python cache files and verify app initialization
"""
import os
import shutil
import sys

def clear_pycache():
    """Remove all __pycache__ directories"""
    removed = []
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            cache_dir = os.path.join(root, '__pycache__')
            try:
                shutil.rmtree(cache_dir)
                removed.append(cache_dir)
                print(f"Removed: {cache_dir}")
            except Exception as e:
                print(f"Error removing {cache_dir}: {e}")
    
    # Also remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.pyc', '.pyo')):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    removed.append(file_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
    
    return removed

def verify_app():
    """Try to import and create the app"""
    try:
        from app import create_app
        app = create_app()
        print("✓ App created successfully!")
        return True
    except AttributeError as e:
        print(f"✗ AttributeError: {e}")
        print("This might be due to cache files. Please restart your Python process.")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == '__main__':
    print("Clearing Python cache files...")
    removed = clear_pycache()
    print(f"\nCleared {len(removed)} cache files/directories\n")
    
    print("Verifying app initialization...")
    success = verify_app()
    
    if success:
        print("\n✓ Everything looks good! You can now run: python app.py")
        sys.exit(0)
    else:
        print("\n✗ There are still issues. Please check the error above.")
        sys.exit(1)
