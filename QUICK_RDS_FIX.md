# 🔧 Quick AWS RDS Fix (Keep Login Screen)

## The Issue

Your `.env` has:
```env
DB_HOST=localhost  ← Wrong! Trying to connect locally
```

Should be:
```env
DB_HOST=your-rds-endpoint.ap-south-1.rds.amazonaws.com  ← Your AWS RDS
```

---

## ⚡ Quick Fix (2 Minutes)

### Step 1: Get Your RDS Endpoint

**From AWS Console:**
1. Go to: https://console.aws.amazon.com/rds/
2. Region: **Asia Pacific (Mumbai)**
3. Click your database
4. Copy **Endpoint** (e.g., `xxx.ap-south-1.rds.amazonaws.com`)

### Step 2: SSH to Your Azure Server

```bash
ssh azureuser@your-azure-ip
cd /home/azureuser/project-python-earthquake-damage-assessment
```

### Step 3: Update .env File

```bash
# Backup current .env
cp .env .env.backup

# Edit .env
nano .env
```

**Change these lines:**
```env
DB_HOST=your-rds-endpoint.ap-south-1.rds.amazonaws.com
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_NAME=earthquake_db
```

**Make sure these lines are NOT present:**
```env
# DEV_MODE=true        ← Remove this!
# BYPASS_AUTH=true     ← Remove this!
```

**Save:** `Ctrl+X`, then `Y`, then `Enter`

### Step 4: Test Connection

```bash
source myenv/bin/activate

python3 << 'EOF'
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("✅ Connected to AWS RDS successfully!")
    conn.close()
except Exception as e:
    print(f"❌ Failed: {e}")
EOF
```

### Step 5: Restart App

```bash
pkill -f gunicorn
nohup gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app > app.log 2>&1 &

# Check logs
tail -f app.log
```

**Press `Ctrl+C` to exit logs**

### Step 6: Test

Visit: `http://your-server-ip:5000`

- ✅ You should see the **login screen**
- ✅ **No more** `ConnectionRefusedError`

---

## 🚀 Or Use My Script

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

# Make executable
chmod +x fix_rds_only.sh

# Run it (will prompt for RDS details)
./fix_rds_only.sh
```

This script will:
- ✅ Ask for your RDS endpoint
- ✅ Update .env with correct config
- ✅ Test the connection
- ✅ Restart your app
- ✅ **Keep login screen active**

---

## 🛡️ Security Group Check

If connection still fails, check RDS security group:

### Get Your Azure VM IP:
```bash
curl ifconfig.me
```

### Add to RDS Security Group:

1. **AWS Console** → EC2 → Security Groups
2. Find your RDS security group
3. **Inbound rules** → Edit inbound rules
4. **Add rule:**
   - Type: `MySQL/Aurora`
   - Port: `3306`
   - Source: `Your-Azure-IP/32`
5. **Save rules**

---

## 📋 Correct .env File Template

```env
# Flask Config
SECRET_KEY=your-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS RDS Database
DB_HOST=your-db.xxxxxx.ap-south-1.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_NAME=earthquake_db

# DO NOT ADD:
# DEV_MODE=true
# BYPASS_AUTH=true
```

---

## ✅ Expected Result

After fix:
- ✅ App connects to AWS RDS
- ✅ Login screen loads normally
- ✅ Users must log in (no bypass)
- ✅ No `ConnectionRefusedError`

---

## 🆘 If Still Not Working

Run this diagnostic:

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

echo "=== DIAGNOSTIC ==="
echo ""
echo "1. Your Azure VM IP:"
curl -s ifconfig.me
echo ""
echo ""
echo "2. .env Database Config:"
grep DB_ .env
echo ""
echo "3. Test RDS Port:"
nc -zv $(grep DB_HOST .env | cut -d'=' -f2) 3306
echo ""
echo "4. Python Connection Test:"
source myenv/bin/activate && python3 test_db_connection.py
echo ""
echo "5. App Logs (last 20 lines):"
tail -20 app.log
```

Send me the output if still failing!

---

**TL;DR:**
1. Get RDS endpoint from AWS Console
2. Edit `.env` → Change `DB_HOST=localhost` to your RDS endpoint
3. Restart: `pkill -f gunicorn && gunicorn --bind 0.0.0.0:5000 wsgi:app &`
4. Login screen will work normally! ✅

