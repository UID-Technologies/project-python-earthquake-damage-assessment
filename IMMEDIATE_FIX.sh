#!/bin/bash
# IMMEDIATE FIX - Update .env and restart

echo "=========================================="
echo "IMMEDIATE DATABASE FIX"
echo "=========================================="
echo ""

cd /home/azureuser/project-python-earthquake-damage-assessment || exit 1

# Show current config
echo "Current .env configuration:"
echo "---"
if [ -f ".env" ]; then
    grep -E "^DB_" .env || echo "No DB_ variables found!"
else
    echo ".env file not found!"
fi
echo "---"
echo ""

# Backup
cp .env .env.backup.old 2>/dev/null

echo "CRITICAL: Your app is trying to connect to 'localhost'"
echo "You need to provide your AWS RDS endpoint"
echo ""
echo "To find it:"
echo "1. Go to: https://console.aws.amazon.com/rds/"
echo "2. Region: Asia Pacific (Mumbai)"
echo "3. Click your database → Copy 'Endpoint'"
echo ""

read -p "Enter AWS RDS Endpoint: " RDS_ENDPOINT

if [ -z "$RDS_ENDPOINT" ]; then
    echo "❌ No endpoint provided. Exiting."
    exit 1
fi

read -p "Enter RDS Username [admin]: " RDS_USER
RDS_USER=${RDS_USER:-admin}

read -sp "Enter RDS Password: " RDS_PASS
echo ""

read -p "Enter Database Name [earthquake_db]: " DB_NAME
DB_NAME=${DB_NAME:-earthquake_db}

# Create new .env
cat > .env << EOF
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "supersecretkey123")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DB_HOST=$RDS_ENDPOINT
DB_PORT=3306
DB_USER=$RDS_USER
DB_PASSWORD=$RDS_PASS
DB_NAME=$DB_NAME
EOF

echo ""
echo "✅ Created new .env file"
echo ""
echo "New configuration:"
grep -E "^DB_" .env
echo ""

# Quick test
echo "Testing connection..."
source myenv/bin/activate

python3 << 'PYEOF'
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

print(f"Attempting to connect to: {os.getenv('DB_HOST')}")

try:
    conn = pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        connect_timeout=10
    )
    print("✅ CONNECTION SUCCESSFUL!")
    conn.close()
    exit(0)
except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
    print("\nPossible issues:")
    print("1. RDS endpoint is incorrect")
    print("2. Username/password is wrong")
    print("3. Security group doesn't allow your IP")
    print(f"4. Database '{os.getenv('DB_NAME')}' doesn't exist")
    exit(1)
PYEOF

if [ $? -eq 0 ]; then
    echo ""
    echo "Restarting application..."
    pkill -f gunicorn
    pkill -f "python.*app"
    sleep 2
    
    source myenv/bin/activate
    nohup gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app > app.log 2>&1 &
    
    sleep 3
    
    echo ""
    echo "=========================================="
    echo "✅ FIXED!"
    echo "=========================================="
    echo ""
    echo "App is now running with AWS RDS"
    echo "Check logs: tail -f app.log"
    echo "Test: curl http://localhost:5000"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ CONNECTION FAILED"
    echo "=========================================="
    echo ""
    echo "DO NOT restart the app yet!"
    echo "Fix the connection issue first."
    echo ""
    echo "Check:"
    echo "1. Is RDS endpoint correct?"
    echo "2. Can you connect manually?"
    echo "   mysql -h $RDS_ENDPOINT -u $RDS_USER -p $DB_NAME"
    echo ""
fi

