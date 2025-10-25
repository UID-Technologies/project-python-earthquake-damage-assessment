#!/bin/bash
# Quick Login Bypass Setup

echo "=========================================="
echo "TEMPORARY LOGIN BYPASS SETUP"
echo "⚠️  FOR DEVELOPMENT ONLY"
echo "=========================================="

cd /home/azureuser/project-python-earthquake-damage-assessment || exit

# Method 1: Add test route
echo ""
echo "[1/4] Adding bypass route..."

if grep -q "dev-login" app/routes/api/auth_api.py; then
    echo "✅ Bypass route already exists"
else
    cat >> app/routes/api/auth_api.py << 'EOF'


# ==========================================
# TEMPORARY BYPASS - REMOVE IN PRODUCTION!
# ==========================================
@auth_api_bp.route("/dev-login", methods=["GET", "POST"])
def dev_login():
    """Development login bypass - WARNING: REMOVE IN PRODUCTION!"""
    from flask import request
    from flask_jwt_extended import create_access_token
    
    username = request.json.get("username", "devuser") if request.is_json else "devuser"
    
    test_user = {
        "user_id": 999,
        "username": username,
        "name": "Development User",
        "email": f"{username}@dev.local"
    }
    
    access_token = create_access_token(identity=test_user)
    
    return jsonify({
        "success": True,
        "token": access_token,
        "user": test_user,
        "message": "⚠️ DEVELOPMENT LOGIN - AUTH BYPASSED"
    }), 200
EOF
    echo "✅ Added bypass route"
fi

# Method 2: Add redirect on homepage
echo ""
echo "[2/4] Adding homepage redirect..."

if grep -q "DEV_MODE" app/routes/pages/auth_pages.py; then
    echo "✅ Redirect already configured"
else
    # Backup original
    cp app/routes/pages/auth_pages.py app/routes/pages/auth_pages.py.backup
    
    cat > app/routes/pages/auth_pages.py << 'EOF'
"""
Authentication Page Routes
Serves HTML pages for login and signup
"""
from flask import Blueprint, render_template, redirect
import os

auth_pages_bp = Blueprint("auth_pages", __name__)


@auth_pages_bp.route("/", methods=["GET"])
def login_page():
    """Render login page - with dev mode bypass"""
    # TEMPORARY: Skip login in dev mode
    if os.getenv("DEV_MODE", "").lower() == "true":
        return redirect("/dashboard")
    
    return render_template("login.html")


@auth_pages_bp.route("/signup", methods=["GET"])
def signup_page():
    """Render signup page"""
    return render_template("signup.html")
EOF
    echo "✅ Added redirect for dev mode"
fi

# Method 3: Set environment variable
echo ""
echo "[3/4] Setting DEV_MODE..."

if grep -q "DEV_MODE=true" .env; then
    echo "✅ DEV_MODE already set"
else
    echo "DEV_MODE=true" >> .env
    echo "✅ Added DEV_MODE=true to .env"
fi

# Restart app
echo ""
echo "[4/4] Restarting application..."
pkill -f gunicorn 2>/dev/null
pkill -f "python.*app.py" 2>/dev/null
sleep 2

source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app > app.log 2>&1 &

sleep 3

echo ""
echo "=========================================="
echo "✅ LOGIN BYPASS ENABLED!"
echo "=========================================="
echo ""
echo "Test methods:"
echo ""
echo "1. Get auto-token:"
echo "   curl http://localhost:5000/api/auth/dev-login"
echo ""
echo "2. Visit homepage (auto-redirects):"
echo "   http://your-server-ip:5000/"
echo ""
echo "3. Go directly to dashboard:"
echo "   http://your-server-ip:5000/dashboard"
echo ""
echo "=========================================="
echo "⚠️  TO REMOVE BYPASS:"
echo "   1. nano .env (remove DEV_MODE=true)"
echo "   2. nano app/routes/api/auth_api.py (delete dev-login)"
echo "   3. mv app/routes/pages/auth_pages.py.backup app/routes/pages/auth_pages.py"
echo "   4. Restart: pkill -f gunicorn && gunicorn wsgi:app"
echo "=========================================="

