#!/bin/bash
# Fix AWS RDS Connection - Keep Login Screen

echo "==========================================="
echo "  AWS RDS DATABASE FIX"
echo "  (Login screen will remain active)"
echo "==========================================="
echo ""

cd /home/azureuser/project-python-earthquake-damage-assessment || exit 1

# Backup .env
if [ -f ".env" ]; then
    cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
    echo "✅ Backed up .env"
fi

echo ""
echo "Enter your AWS RDS details:"
echo ""

# Get RDS details
read -p "RDS Endpoint (e.g., xxx.ap-south-1.rds.amazonaws.com): " RDS_HOST
read -p "RDS Username [admin]: " RDS_USER
RDS_USER=${RDS_USER:-admin}
read -sp "RDS Password: " RDS_PASS
echo ""
read -p "Database Name [earthquake_db]: " DB_NAME
DB_NAME=${DB_NAME:-earthquake_db}

# Generate secret key if needed
if [ -f ".env" ] && grep -q "SECRET_KEY=" .env; then
    SECRET_KEY=$(grep "SECRET_KEY=" .env | cut -d'=' -f2)
else
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || openssl rand -hex 32)
fi

# Create .env - NO DEV_MODE, NO BYPASS
cat > .env << EOF
# Flask Configuration
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS RDS Database (Mumbai Region)
DB_HOST=$RDS_HOST
DB_PORT=3306
DB_USER=$RDS_USER
DB_PASSWORD=$RDS_PASS
DB_NAME=$DB_NAME
EOF

echo ""
echo "✅ Updated .env with AWS RDS configuration"
echo ""
echo "Configuration:"
echo "  DB_HOST: $RDS_HOST"
echo "  DB_USER: $RDS_USER"
echo "  DB_NAME: $DB_NAME"

# Test connection
echo ""
echo "Testing connection..."
source myenv/bin/activate

python3 << 'PYTEST'
import pymysql, os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connect_timeout=10
    )
    print("✅ AWS RDS connection successful!")
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    print(f"✅ MySQL version: {cursor.fetchone()[0]}")
    conn.close()
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nCheck:")
    print("1. RDS endpoint and credentials are correct")
    print("2. RDS security group allows your IP")
    print(f"   Your IP: $(curl -s ifconfig.me)")
PYTEST

if [ $? -eq 0 ]; then
    echo ""
    echo "Restarting application..."
    pkill -f gunicorn 2>/dev/null
    pkill -f "python.*app" 2>/dev/null
    sleep 2
    
    source myenv/bin/activate
    nohup gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app > app.log 2>&1 &
    
    sleep 3
    
    echo ""
    echo "==========================================="
    echo "✅ DONE!"
    echo "==========================================="
    echo ""
    echo "Database: Connected to AWS RDS"
    echo "Login: Normal login screen active"
    echo ""
    echo "Access: http://your-server-ip:5000"
    echo "Logs: tail -f app.log"
    echo ""
else
    echo ""
    echo "⚠️  Connection test failed"
    echo "    Fix connection issues before restarting app"
fi

