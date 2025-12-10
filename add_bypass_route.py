#!/usr/bin/env python3
"""
Quick script to add login bypass route
Run: python3 add_bypass_route.py
"""

import os

# Code to add to auth_api.py
bypass_code = '''

# ==========================================
# TEMPORARY BYPASS - REMOVE IN PRODUCTION!
# ==========================================
@auth_api_bp.route("/dev-login", methods=["GET", "POST"])
def dev_login():
    """
    Development login bypass
    WARNING: REMOVE THIS IN PRODUCTION!
    
    Usage:
    - GET: Returns a test token
    - POST: Can accept username (optional)
    """
    from flask import request
    from flask_jwt_extended import create_access_token
    
    # Get username from request or use default
    username = request.json.get("username", "devuser") if request.is_json else "devuser"
    
    # Create test user
    test_user = {
        "user_id": 999,
        "username": username,
        "name": "Development User",
        "email": f"{username}@dev.local"
    }
    
    # Create access token
    access_token = create_access_token(identity=test_user)
    
    return jsonify({
        "success": True,
        "token": access_token,
        "user": test_user,
        "message": "⚠️ DEVELOPMENT LOGIN - AUTH BYPASSED"
    }), 200
'''

# Path to auth_api.py
auth_file = "app/routes/api/auth_api.py"

if os.path.exists(auth_file):
    with open(auth_file, 'r') as f:
        content = f.read()
    
    # Check if already added
    if "dev-login" in content:
        print("✅ Bypass route already exists!")
    else:
        # Add to end of file
        with open(auth_file, 'a') as f:
            f.write(bypass_code)
        print("✅ Added bypass route to", auth_file)
        print("\n📍 Test with:")
        print("   curl http://localhost:5000/api/auth/dev-login")
        print("\n⚠️  Remember to remove this in production!")
else:
    print(f"❌ File not found: {auth_file}")
    print("   Make sure you're in the project root directory")

