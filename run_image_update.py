#!/usr/bin/env python3
"""
Simple script to run the product image update.
Run this from the project root directory.
"""

import subprocess
import sys
import os

def main():
    print("🚀 Musical Instruments Platform - Product Image Update")
    print("=" * 60)
    
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    
    try:
        print("📂 Changing to backend directory...")
        os.chdir(backend_dir)
        
        print("🔄 Running product image update script...")
        result = subprocess.run([
            sys.executable, 
            "scripts/update_product_images.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Update completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Update failed!")
            print("\nError:")
            print(result.stderr)
            return 1
            
    except Exception as e:
        print(f"❌ Error running update: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())