# 🚀 Azure Server Quick Fix - Database Connection

## Your Issue
```
ConnectionRefusedError: [Errno 111] Connection refused
```

Your Flask app **CAN'T connect to MySQL** on your Azure server.

---

## ⚡ QUICK FIX (Run These Commands)

### Step 1: Check MySQL Status

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment
sudo systemctl status mysql
```

**If MySQL is NOT running or NOT installed:**

```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server -y

# Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Check it's running
sudo systemctl status mysql
```

### Step 2: Run Quick Fix Script

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

# Make script executable
chmod +x quick_fix_db.sh

# Run it
./quick_fix_db.sh
```

### Step 3: If Password is Needed

```bash
# Set MySQL root password (if not set)
sudo mysql

# In MySQL prompt:
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'YourPassword123';
FLUSH PRIVILEGES;
EXIT;

# Update .env file
nano .env

# Change this line:
DB_PASSWORD=YourPassword123
```

### Step 4: Create Database Manually

```bash
sudo mysql << 'EOF'
CREATE DATABASE IF NOT EXISTS earthquake_db;
SHOW DATABASES;
EXIT
EOF
```

### Step 5: Test Connection

```bash
# Activate virtual environment
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate

# Test connection
python3 << 'EOF'
import pymysql
import os

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Add password if you set one
        database='earthquake_db'
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Failed: {e}")
EOF
```

### Step 6: Restart Your App

```bash
# Find running processes
ps aux | grep gunicorn
ps aux | grep python

# Kill them
pkill -f gunicorn
pkill -f "python.*app.py"

# Restart app
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate

# Option A: Using gunicorn (recommended)
nohup gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app > app.log 2>&1 &

# Option B: Using Flask directly
nohup python3 app.py > app.log 2>&1 &

# Check logs
tail -f app.log
```

---

## 🎯 Most Common Solution (90% of cases)

```bash
# Just start MySQL!
sudo systemctl start mysql
sudo systemctl enable mysql

# Create database
sudo mysql -e "CREATE DATABASE IF NOT EXISTS earthquake_db;"

# Restart your app
pkill -f gunicorn
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &

# Test
curl http://localhost:5000
```

---

## 🔍 If Still Failing - Check These

### 1. Check .env file exists:
```bash
cat /home/azureuser/project-python-earthquake-damage-assessment/.env
```

Should contain:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=earthquake_db
```

### 2. Check MySQL is listening:
```bash
sudo netstat -tlnp | grep 3306
# Should show: 0.0.0.0:3306 or 127.0.0.1:3306
```

### 3. Check pymysql is installed:
```bash
source myenv/bin/activate
pip list | grep -i mysql
# Should show: PyMySQL
```

If not:
```bash
pip install pymysql
```

### 4. Check app can read .env:
```bash
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('DB_HOST'))"
# Should print: localhost
```

---

## 📞 One-Liner Fix

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment && sudo systemctl start mysql && sudo mysql -e "CREATE DATABASE IF NOT EXISTS earthquake_db;" && pkill -f gunicorn && source myenv/bin/activate && nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 & && sleep 2 && curl http://localhost:5000
```

---

## ✅ Success Indicators

After fix, you should see:
```bash
tail -f app.log
```

**Good output:**
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:5000
[INFO] Booting worker
```

**NO MORE:**
```
ConnectionRefusedError
```

---

## 🆘 Still Not Working?

Run this diagnostic:
```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

echo "=== DIAGNOSTIC ==="
echo "1. MySQL status:"
sudo systemctl status mysql | head -5

echo ""
echo "2. .env file:"
cat .env | grep DB_

echo ""
echo "3. Can connect to MySQL:"
mysql -h localhost -u root -p -e "SELECT 1;" 2>&1 | head -2

echo ""
echo "4. pymysql installed:"
source myenv/bin/activate && pip list | grep -i pymysql

echo ""
echo "5. App process:"
ps aux | grep -E "gunicorn|python.*app.py" | grep -v grep
```

**Send me this output if still failing!**

---

**TL;DR**: MySQL is not running. Start it with `sudo systemctl start mysql`

