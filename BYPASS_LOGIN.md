# 🔓 Temporary Login Bypass Methods

## ⚠️ WARNING: FOR TESTING ONLY - DISABLE IN PRODUCTION!

---

## Method 1: Environment Variable Bypass (Recommended) ⭐

### Step 1: Add to .env file

```bash
nano .env
```

Add this line:
```env
DEV_MODE=true
BYPASS_AUTH=true
```

### Step 2: Update config.py

```python
# Add to app/config.py
class Config:
    # ... existing config ...
    DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"
    BYPASS_AUTH = os.getenv("BYPASS_AUTH", "false").lower() == "true"
```

### Step 3: Create auth bypass decorator

Create file: `app/auth_utils.py`

```python
from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.config import Config

def jwt_required_with_bypass():
    """JWT required decorator with bypass option for dev"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if Config.BYPASS_AUTH:
                # Skip authentication in dev mode
                return fn(*args, **kwargs)
            else:
                # Normal JWT authentication
                return jwt_required()(fn)(*args, **kwargs)
        return wrapper
    return decorator
```

### Step 4: Replace @jwt_required() decorators

This is the slow way. Skip to Method 2 for faster solution!

---

## Method 2: Quick Dashboard Redirect (FASTEST) ⚡

### Just redirect root to dashboard directly:

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment
```

Edit `app/routes/pages/auth_pages.py`:

```python
from flask import Blueprint, render_template, redirect, url_for
import os

auth_pages_bp = Blueprint("auth_pages", __name__)

@auth_pages_bp.route("/", methods=["GET"])
def login_page():
    """Render login page - BYPASS if DEV_MODE"""
    # TEMPORARY BYPASS
    if os.getenv("DEV_MODE", "").lower() == "true":
        return redirect("/dashboard")
    
    return render_template("login.html")

@auth_pages_bp.route("/signup", methods=["GET"])
def signup_page():
    """Render signup page"""
    return render_template("signup.html")
```

Then add to `.env`:
```bash
echo "DEV_MODE=true" >> .env
```

Restart app:
```bash
pkill -f gunicorn
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &
```

---

## Method 3: Auto-Login Test Route (EASIEST) 🎯

### Create a test login route:

Edit `app/routes/api/auth_api.py` and add:

```python
@auth_api_bp.route("/test-login", methods=["GET", "POST"])
def test_login():
    """
    TEMPORARY: Auto-login for testing
    WARNING: REMOVE IN PRODUCTION!
    """
    from flask_jwt_extended import create_access_token
    
    # Create token for test user
    test_user = {
        "user_id": 1,
        "username": "testuser",
        "name": "Test User"
    }
    
    access_token = create_access_token(identity=test_user)
    
    return jsonify({
        "success": True,
        "token": access_token,
        "user": test_user,
        "message": "⚠️ TEST LOGIN - BYPASS ENABLED"
    }), 200
```

### Then access:
```
http://your-server-ip:5000/api/auth/test-login
```

Copy the token and use it in your requests.

---

## Method 4: Disable JWT Check Globally (NUCLEAR OPTION) 💣

### Edit `app/__init__.py`:

```python
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # TEMPORARY: Skip JWT in dev mode
    if Config.DEV_MODE:
        # Don't initialize JWT
        print("⚠️ WARNING: JWT AUTHENTICATION DISABLED - DEV MODE")
    else:
        jwt.init_app(app)
    
    bcrypt.init_app(app)
    
    # ... rest of code ...
```

Add to `.env`:
```
DEV_MODE=true
```

⚠️ **This breaks all @jwt_required() routes!**

---

## Method 5: Frontend JavaScript Bypass (QUICKEST!) ⚡⚡⚡

### Just skip the login form validation:

Edit `app/static/js/login.js`:

Add at the top:

```javascript
// TEMPORARY BYPASS - REMOVE IN PRODUCTION
if (window.location.hostname === 'localhost' || window.location.search.includes('bypass=true')) {
    console.warn('⚠️ AUTH BYPASS ENABLED');
    localStorage.setItem('token', 'bypass-token-dev-only');
    localStorage.setItem('user', JSON.stringify({id: 1, username: 'dev', name: 'Developer'}));
    window.location.href = '/dashboard';
}
```

Or just visit:
```
http://your-server:5000/?bypass=true
```

---

## 🚀 RECOMMENDED QUICK FIX (30 seconds)

Run this on your server:

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

# Add bypass to .env
echo "DEV_MODE=true" >> .env

# Create test login route
cat >> app/routes/api/auth_api.py << 'EOF'

@auth_api_bp.route("/dev-login", methods=["GET"])
def dev_login():
    """TEMP: Skip login for development"""
    from flask_jwt_extended import create_access_token
    token = create_access_token(identity={"user_id": 999, "username": "dev", "name": "Developer"})
    return jsonify({"success": True, "token": token}), 200
EOF

# Restart app
pkill -f gunicorn
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &

# Get token
curl http://localhost:5000/api/auth/dev-login
```

Copy the token from the response and use it!

---

## 🔒 RE-ENABLE SECURITY LATER

Remove from `.env`:
```bash
nano .env
# Delete line: DEV_MODE=true
```

Remove test routes:
```bash
# Edit auth_api.py and delete the dev-login function
nano app/routes/api/auth_api.py
```

Restart:
```bash
pkill -f gunicorn
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &
```

---

## ✅ Choose Your Method:

- **Fastest**: Method 5 (Frontend bypass)
- **Safest**: Method 1 (Environment variable)
- **Easiest**: Method 3 (Test route)
- **Recommended**: Method 3 (adds a `/dev-login` endpoint)

---

**Remember**: All these are TEMPORARY for testing. Remove before going to production!

