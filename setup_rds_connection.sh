#!/bin/bash
# Interactive AWS RDS Connection Setup

echo "==========================================="
echo "  AWS RDS CONNECTION SETUP"
echo "  Region: ap-south-1 (Mumbai)"
echo "==========================================="
echo ""

# Get current directory
cd /home/azureuser/project-python-earthquake-damage-assessment || {
    echo "❌ Project directory not found!"
    exit 1
}

# Backup existing .env
if [ -f ".env" ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backed up existing .env"
fi

echo ""
echo "Enter your AWS RDS details:"
echo "(Find these in AWS Console → RDS → Your Database)"
echo ""

# Prompt for RDS details
read -p "RDS Endpoint (e.g., xxx.ap-south-1.rds.amazonaws.com): " RDS_HOST
read -p "RDS Username [admin]: " RDS_USER
RDS_USER=${RDS_USER:-admin}
read -sp "RDS Password: " RDS_PASS
echo ""
read -p "Database Name [earthquake_db]: " DB_NAME
DB_NAME=${DB_NAME:-earthquake_db}
read -p "RDS Port [3306]: " DB_PORT
DB_PORT=${DB_PORT:-3306}

# Generate secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -hex 32)

# Create .env file
cat > .env << EOF
# ==========================================
# FLASK CONFIGURATION
# ==========================================
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ==========================================
# AWS RDS DATABASE (Mumbai Region)
# ==========================================
DB_HOST=$RDS_HOST
DB_PORT=$DB_PORT
DB_USER=$RDS_USER
DB_PASSWORD=$RDS_PASS
DB_NAME=$DB_NAME

# ==========================================
# OPTIONAL SETTINGS
# ==========================================
# DEV_MODE=false
EOF

echo ""
echo "✅ Created .env file with AWS RDS configuration"

# Show configuration (hide password)
echo ""
echo "Configuration:"
echo "  DB_HOST: $RDS_HOST"
echo "  DB_PORT: $DB_PORT"
echo "  DB_USER: $RDS_USER"
echo "  DB_PASSWORD: ********"
echo "  DB_NAME: $DB_NAME"

# Test network connectivity
echo ""
echo "Testing network connectivity to RDS..."
if command -v nc &> /dev/null; then
    if nc -zv -w 5 "$RDS_HOST" "$DB_PORT" 2>&1 | grep -q "succeeded"; then
        echo "✅ Port $DB_PORT is reachable"
    else
        echo "❌ Cannot reach port $DB_PORT"
        echo "   → Check RDS security group allows your IP"
        echo "   → Your IP: $(curl -s ifconfig.me)"
    fi
else
    echo "⚠️  nc command not found, skipping connectivity test"
fi

# Test Python connection
echo ""
echo "Testing Python database connection..."
source myenv/bin/activate 2>/dev/null

python3 << 'PYTEST'
import sys
try:
    import pymysql
    from dotenv import load_dotenv
    import os

    load_dotenv()

    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connect_timeout=10
    )
    
    print("✅ Database connection SUCCESSFUL!")
    
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL version: {version[0]}")
    
    cursor.execute("SELECT DATABASE()")
    db = cursor.fetchone()
    print(f"✅ Connected to database: {db[0]}")
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    if tables:
        print(f"✅ Found {len(tables)} tables")
        for table in tables:
            print(f"   - {table[0]}")
    else:
        print("⚠️  No tables found (database is empty)")
        print("   You may need to run database migrations")
    
    conn.close()
    sys.exit(0)

except ImportError:
    print("❌ pymysql not installed")
    print("   Run: pip install pymysql")
    sys.exit(1)
except Exception as e:
    print(f"❌ Connection FAILED: {e}")
    print("\nTroubleshooting:")
    print("1. Verify RDS endpoint and credentials")
    print("2. Check RDS security group allows your IP:")
    print(f"   Your IP: $(curl -s ifconfig.me)")
    print("3. Verify RDS is publicly accessible (if needed)")
    print("4. Check if database exists:")
    print(f"   mysql -h {os.getenv('DB_HOST')} -u {os.getenv('DB_USER')} -p -e 'SHOW DATABASES;'")
    sys.exit(1)
PYTEST

if [ $? -eq 0 ]; then
    echo ""
    echo "==========================================="
    echo "✅ AWS RDS CONNECTION SUCCESSFUL!"
    echo "==========================================="
    echo ""
    echo "Restarting application..."
    
    # Stop existing processes
    pkill -f gunicorn 2>/dev/null
    pkill -f "python.*app.py" 2>/dev/null
    sleep 2
    
    # Start application
    source myenv/bin/activate
    nohup gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app > app.log 2>&1 &
    
    sleep 3
    
    echo "✅ Application restarted"
    echo ""
    echo "Check logs: tail -f app.log"
    echo "Test app: curl http://localhost:5000"
    echo ""
else
    echo ""
    echo "==========================================="
    echo "❌ CONNECTION FAILED"
    echo "==========================================="
    echo ""
    echo "Common fixes:"
    echo ""
    echo "1. Add your Azure VM IP to RDS security group:"
    echo "   Your IP: $(curl -s ifconfig.me)"
    echo "   AWS Console → EC2 → Security Groups → Add inbound rule"
    echo "   Type: MySQL/Aurora, Port: 3306, Source: YOUR_IP/32"
    echo ""
    echo "2. Verify RDS is publicly accessible:"
    echo "   AWS Console → RDS → Your DB → Connectivity & security"
    echo "   Public access: Yes"
    echo ""
    echo "3. Test with MySQL client:"
    echo "   mysql -h $RDS_HOST -u $RDS_USER -p $DB_NAME"
    echo ""
    echo "4. Create database if it doesn't exist:"
    echo "   mysql -h $RDS_HOST -u $RDS_USER -p -e 'CREATE DATABASE $DB_NAME;'"
    echo ""
fi

