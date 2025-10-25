# 🔧 Fix AWS RDS Database Connection

## ❌ Current Problem

Your `.env` file is configured for LOCAL database:
```env
DB_HOST=localhost  ← WRONG! This tries to connect to local MySQL
```

But you're using **AWS RDS** (remote database server)!

---

## ✅ Correct Configuration for AWS RDS

### Step 1: Get Your RDS Endpoint

**From AWS Console:**
1. Go to: https://console.aws.amazon.com/rds/
2. Select Region: **Asia Pacific (Mumbai) - ap-south-1**
3. Click on your database instance
4. Copy the **Endpoint** (looks like: `your-db.xxxxx.ap-south-1.rds.amazonaws.com`)

**Or from AWS CLI:**
```bash
aws rds describe-db-instances --region ap-south-1 --query 'DBInstances[0].Endpoint.Address' --output text
```

### Step 2: Update .env File on Azure Server

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

# Backup current .env
cp .env .env.backup

# Create correct .env for AWS RDS
cat > .env << 'EOF'
# Flask Config
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS RDS Database Configuration
DB_HOST=your-rds-endpoint.ap-south-1.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_NAME=earthquake_db

# Dev Mode (optional, for testing)
# DEV_MODE=true
EOF
```

**Replace these values:**
- `your-rds-endpoint` → Your actual RDS endpoint
- `your-rds-password` → Your RDS master password
- `admin` → Your RDS username (might be different)

---

## 🔍 Find Your RDS Details

### Method 1: AWS Console

```
1. AWS Console → RDS → Databases
2. Click your database
3. Look for:
   - Endpoint: xxxxxxxxx.ap-south-1.rds.amazonaws.com
   - Port: 3306
   - Master username: (usually 'admin')
```

### Method 2: Check CloudFormation/Terraform

If you used IaC, check your deployment files for RDS configuration.

### Method 3: Check Your Records

Look for your RDS setup documentation or email from when you created it.

---

## 🛡️ Security Group Configuration

**CRITICAL**: Your Azure VM must be able to reach AWS RDS!

### Check RDS Security Group:

1. AWS Console → RDS → Your Database → Connectivity & security
2. Click on the **VPC security group**
3. Check **Inbound rules**

**Required rule:**
```
Type: MySQL/Aurora
Protocol: TCP
Port: 3306
Source: Your Azure VM's public IP / OR 0.0.0.0/0 (for testing)
```

### Get Your Azure VM's Public IP:

```bash
# On Azure VM
curl ifconfig.me
```

### Add Azure IP to RDS Security Group:

```bash
# AWS CLI
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxxxxxx \
  --protocol tcp \
  --port 3306 \
  --cidr YOUR_AZURE_IP/32 \
  --region ap-south-1
```

Or use AWS Console:
```
1. EC2 → Security Groups → Your RDS security group
2. Inbound rules → Edit inbound rules → Add rule
3. Type: MySQL/Aurora, Source: Custom → YOUR_AZURE_IP/32
4. Save rules
```

---

## 📝 Complete .env Template for AWS RDS

```bash
cat > /home/azureuser/project-python-earthquake-damage-assessment/.env << 'EOF'
# ==========================================
# FLASK APPLICATION CONFIGURATION
# ==========================================
SECRET_KEY=change-this-to-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ==========================================
# AWS RDS DATABASE CONFIGURATION
# Region: Asia Pacific (Mumbai - ap-south-1)
# ==========================================
DB_HOST=earthquake-db.xxxxxxxxx.ap-south-1.rds.amazonaws.com
DB_PORT=3306
DB_USER=admin
DB_PASSWORD=YourRDSPassword123!
DB_NAME=earthquake_db

# ==========================================
# OPTIONAL: DEVELOPMENT MODE
# ==========================================
# DEV_MODE=false
# BYPASS_AUTH=false
EOF
```

**Edit with your actual values:**
```bash
nano .env
```

---

## 🧪 Test RDS Connection

### Test 1: Network Connectivity

```bash
# Test if port 3306 is reachable
nc -zv your-rds-endpoint.ap-south-1.rds.amazonaws.com 3306

# Expected: "Connection to ... 3306 port [tcp/mysql] succeeded!"
# If fails: Security group issue!
```

### Test 2: MySQL Client Connection

```bash
# Install MySQL client if needed
sudo apt update
sudo apt install mysql-client -y

# Test connection
mysql -h your-rds-endpoint.ap-south-1.rds.amazonaws.com \
      -P 3306 \
      -u admin \
      -p \
      earthquake_db

# Enter password when prompted
# If successful: You'll see mysql> prompt
```

### Test 3: Python Connection

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate

python3 << 'EOF'
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print("Testing AWS RDS connection...")
print(f"Host: {os.getenv('DB_HOST')}")
print(f"User: {os.getenv('DB_USER')}")
print(f"Database: {os.getenv('DB_NAME')}")

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connect_timeout=10
    )
    print("✅ SUCCESS: Connected to AWS RDS!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL version: {version[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✅ Tables in database: {len(tables)}")
    
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Check DB_HOST in .env is your RDS endpoint")
    print("2. Check DB_PASSWORD is correct")
    print("3. Check RDS security group allows your Azure IP")
    print("4. Check RDS is publicly accessible (if needed)")
EOF
```

---

## 🚀 Quick Fix Script

```bash
cd /home/azureuser/project-python-earthquake-damage-assessment

# Save this as fix_rds.sh
cat > fix_rds.sh << 'SCRIPT'
#!/bin/bash

echo "==========================================="
echo "AWS RDS CONNECTION SETUP"
echo "==========================================="

# Prompt for RDS details
read -p "Enter RDS Endpoint: " RDS_HOST
read -p "Enter RDS Username [admin]: " RDS_USER
RDS_USER=${RDS_USER:-admin}
read -sp "Enter RDS Password: " RDS_PASS
echo ""
read -p "Enter Database Name [earthquake_db]: " DB_NAME
DB_NAME=${DB_NAME:-earthquake_db}

# Create .env file
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_HOST=$RDS_HOST
DB_PORT=3306
DB_USER=$RDS_USER
DB_PASSWORD=$RDS_PASS
DB_NAME=$DB_NAME
EOF

echo ""
echo "✅ Created .env file"

# Test connection
echo ""
echo "Testing connection..."
python3 << 'PYTEST'
import pymysql, os
from dotenv import load_dotenv
load_dotenv()
try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
PYTEST

echo ""
echo "Restarting application..."
pkill -f gunicorn
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &

echo ""
echo "✅ Done! Check logs: tail -f app.log"
SCRIPT

chmod +x fix_rds.sh
./fix_rds.sh
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Connection timed out"
**Cause**: Security group not allowing your IP
**Fix**: Add Azure VM IP to RDS security group inbound rules

### Issue 2: "Access denied for user"
**Cause**: Wrong username/password
**Fix**: Check RDS master username and reset password if needed

### Issue 3: "Unknown database"
**Cause**: Database doesn't exist
**Fix**: Create it:
```bash
mysql -h your-rds-endpoint -u admin -p -e "CREATE DATABASE earthquake_db;"
```

### Issue 4: "Can't connect - SSL required"
**Cause**: RDS requires SSL
**Fix**: Add to connection:
```python
conn = pymysql.connect(..., ssl={'ssl': True})
```

---

## 📋 Checklist

- [ ] Get RDS endpoint from AWS Console
- [ ] Get RDS username (usually 'admin')
- [ ] Get/reset RDS password
- [ ] Update .env file with RDS details
- [ ] Add Azure VM IP to RDS security group
- [ ] Test connection with mysql client
- [ ] Test connection with Python script
- [ ] Restart Flask application
- [ ] Check logs for connection success

---

## 🔗 Useful AWS CLI Commands

```bash
# List RDS instances
aws rds describe-db-instances --region ap-south-1

# Get endpoint
aws rds describe-db-instances \
  --region ap-south-1 \
  --query 'DBInstances[0].Endpoint.Address' \
  --output text

# Get security group
aws rds describe-db-instances \
  --region ap-south-1 \
  --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' \
  --output text
```

---

**After configuring, restart your app:**
```bash
pkill -f gunicorn
cd /home/azureuser/project-python-earthquake-damage-assessment
source myenv/bin/activate
nohup gunicorn --bind 0.0.0.0:5000 wsgi:app > app.log 2>&1 &
tail -f app.log
```

**Connection should now work!** ✅

