# 🔧 Database Connection Troubleshooting Guide

## Error Summary

```
ConnectionRefusedError: [Errno 111] Connection refused
```

Your Flask application is **running fine**, but it **cannot connect to the MySQL database**. This means:
- ✅ Flask app is working
- ✅ Python environment is correct
- ❌ MySQL connection is refused

---

## 🔍 Common Causes & Solutions

### 1. MySQL Server Not Running

**Check if MySQL is running:**

```bash
# Check MySQL status
sudo systemctl status mysql

# Or for MariaDB
sudo systemctl status mariadb

# Check if MySQL process is running
ps aux | grep mysql
```

**If not running, start it:**

```bash
# Start MySQL
sudo systemctl start mysql

# Enable auto-start on boot
sudo systemctl enable mysql

# Check status again
sudo systemctl status mysql
```

---

### 2. Wrong Database Host Configuration

**Check your environment variables:**

```bash
# View your current config
cd /home/azureuser/project-python-earthquake-damage-assessment
cat .env

# Or check what the app sees
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'DB_HOST: {os.getenv(\"DB_HOST\", \"localhost\")}')"
```

**Common issues:**

| Your Config | Should Be | Notes |
|-------------|-----------|-------|
| `DB_HOST=localhost` | ✅ Correct | If MySQL is on same server |
| `DB_HOST=127.0.0.1` | ✅ Correct | Same as localhost |
| `DB_HOST=db` | ❌ Wrong | Only for Docker Compose |
| `DB_HOST=your-rds-endpoint` | ✅ Correct | If using AWS RDS |

**Fix if needed:**

```bash
# Edit .env file
nano .env

# Make sure DB_HOST is correct:
DB_HOST=localhost        # If MySQL is on same server
DB_HOST=127.0.0.1        # Alternative
# OR
DB_HOST=your-actual-mysql-host    # If remote
```

---

### 3. MySQL Not Listening on Expected Port

**Check what port MySQL is using:**

```bash
# Check MySQL port (default is 3306)
sudo netstat -tlnp | grep mysql

# Or
sudo ss -tlnp | grep mysql

# Check MySQL config
sudo cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep port
```

**If MySQL is on different port, update .env:**

```bash
DB_PORT=3307  # Or whatever port MySQL is using
```

---

### 4. MySQL Not Configured for Network Connections

**Check MySQL bind address:**

```bash
# Check if MySQL is only listening on localhost
sudo cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep bind-address
```

**If you see `bind-address = 127.0.0.1`:**

This is correct if your app is on the same server. If not:

```bash
# Edit MySQL config
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

# Change:
bind-address = 127.0.0.1

# To:
bind-address = 0.0.0.0

# Save and restart MySQL
sudo systemctl restart mysql
```

⚠️ **Security Note**: Only do this if you need remote connections, and use firewall rules!

---

### 5. Firewall Blocking Connection

**Check firewall status:**

```bash
# Check if firewall is active
sudo ufw status

# Check iptables
sudo iptables -L -n
```

**If firewall is blocking, allow MySQL:**

```bash
# Allow MySQL port
sudo ufw allow 3306/tcp

# Or for specific IP only (more secure)
sudo ufw allow from YOUR_APP_IP to any port 3306
```

---

### 6. MySQL User Permissions

**Check if database user has proper permissions:**

```bash
# Login to MySQL as root
sudo mysql -u root -p

# Or without password (if configured)
sudo mysql

# Check user permissions
SELECT user, host FROM mysql.user;

# Grant permissions if needed
GRANT ALL PRIVILEGES ON earthquake_db.* TO 'root'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;

# Exit
EXIT;
```

---

### 7. Database Doesn't Exist

**Check if database exists:**

```bash
# Login to MySQL
sudo mysql -u root -p

# List databases
SHOW DATABASES;

# If earthquake_db doesn't exist, create it:
CREATE DATABASE earthquake_db;

# Exit
EXIT;
```

---

## 🚀 Quick Fix Commands (Try These First)

Run these commands on your Azure server:

```bash
# 1. Check if MySQL is running
sudo systemctl status mysql

# 2. If not running, start it
sudo systemctl start mysql

# 3. Test connection manually
mysql -h localhost -u root -p

# 4. If that works, test from Python
python3 << EOF
import pymysql
try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='YOUR_PASSWORD',
        database='earthquake_db'
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
EOF
```

---

## 🔧 Complete Diagnostic Script

Create and run this script on your server:

```bash
# Create diagnostic script
cat > check_db.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import socket
from dotenv import load_dotenv

load_dotenv()

print("="*60)
print("DATABASE CONNECTION DIAGNOSTICS")
print("="*60)

# Get config
db_host = os.getenv('DB_HOST', 'localhost')
db_port = int(os.getenv('DB_PORT', 3306))
db_user = os.getenv('DB_USER', 'root')
db_name = os.getenv('DB_NAME', 'earthquake_db')

print(f"\n[*] Configuration:")
print(f"    DB_HOST: {db_host}")
print(f"    DB_PORT: {db_port}")
print(f"    DB_USER: {db_user}")
print(f"    DB_NAME: {db_name}")

# Test 1: Port connectivity
print(f"\n[*] Testing port connectivity to {db_host}:{db_port}...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((db_host, db_port))
    sock.close()
    
    if result == 0:
        print(f"    ✅ Port {db_port} is OPEN")
    else:
        print(f"    ❌ Port {db_port} is CLOSED or FILTERED")
        print(f"    → Check if MySQL is running: sudo systemctl status mysql")
        print(f"    → Check firewall: sudo ufw status")
except Exception as e:
    print(f"    ❌ Connection test failed: {e}")

# Test 2: MySQL connection
print(f"\n[*] Testing MySQL connection...")
try:
    import pymysql
    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=os.getenv('DB_PASSWORD', ''),
        database=db_name,
        connect_timeout=5
    )
    print(f"    ✅ MySQL connection SUCCESSFUL!")
    conn.close()
except ImportError:
    print(f"    ⚠️  pymysql not installed")
    print(f"    → Install: pip install pymysql")
except Exception as e:
    print(f"    ❌ MySQL connection FAILED: {e}")
    print(f"\n[*] Troubleshooting:")
    print(f"    1. Check MySQL is running: sudo systemctl status mysql")
    print(f"    2. Check credentials in .env file")
    print(f"    3. Check database exists: mysql -u root -p -e 'SHOW DATABASES;'")
    print(f"    4. Check user permissions")

print("\n" + "="*60)
EOF

# Run diagnostic
python3 check_db.py
```

---

## 🎯 Step-by-Step Fix (Most Common Solution)

### For Localhost MySQL (Same Server)

```bash
# 1. Navigate to project directory
cd /home/azureuser/project-python-earthquake-damage-assessment

# 2. Check if MySQL is installed
which mysql

# 3. Install if needed
sudo apt update
sudo apt install mysql-server -y

# 4. Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# 5. Secure MySQL (set root password)
sudo mysql_secure_installation

# 6. Create database and user
sudo mysql << EOF
CREATE DATABASE IF NOT EXISTS earthquake_db;
CREATE USER IF NOT EXISTS 'earthquake_user'@'localhost' IDENTIFIED BY 'SecurePassword123!';
GRANT ALL PRIVILEGES ON earthquake_db.* TO 'earthquake_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
EOF

# 7. Update .env file
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DB_HOST=localhost
DB_PORT=3306
DB_USER=earthquake_user
DB_PASSWORD=SecurePassword123!
DB_NAME=earthquake_db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EOF

# 8. Test connection
python3 test_db_connection.py

# 9. Restart your app
pkill -f gunicorn
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &
```

---

## 🐳 For Docker Deployment

If you're using Docker Compose, the database connection should use:

```env
DB_HOST=db          # Service name from docker-compose.yml
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=earthquake_db
```

---

## ⚠️ If Using AWS RDS or Remote MySQL

```bash
# Update .env with remote host
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_NAME=earthquake_db

# Make sure security group allows connection from your server IP
# In AWS console: RDS → Your DB → Security → Inbound rules → Add your server IP
```

---

## 📊 Connection Test Script

Quick test without running the full app:

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate

python3 << EOF
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'earthquake_db')
    )
    print("✅ SUCCESS: Database connection working!")
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL version: {version[0]}")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. sudo systemctl status mysql")
    print("2. Check .env file has correct credentials")
    print("3. mysql -h localhost -u root -p")
EOF
```

---

## 🔑 Summary Checklist

- [ ] MySQL server is installed
- [ ] MySQL service is running (`sudo systemctl status mysql`)
- [ ] Database `earthquake_db` exists
- [ ] User has proper permissions
- [ ] `.env` file has correct `DB_HOST=localhost`
- [ ] Port 3306 is open (check firewall)
- [ ] Can connect manually: `mysql -h localhost -u root -p`

---

**Most Common Fix**: Start MySQL service!

```bash
sudo systemctl start mysql
sudo systemctl enable mysql
```

Then restart your Flask app.

---

**Need More Help?** Run the diagnostic script above and share the output!

