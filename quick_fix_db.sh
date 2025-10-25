#!/bin/bash
# Quick Database Connection Fix for Azure Server

echo "=========================================="
echo "DATABASE CONNECTION QUICK FIX"
echo "=========================================="

# Check if MySQL is installed
echo ""
echo "[1/6] Checking MySQL installation..."
if command -v mysql &> /dev/null; then
    echo "✅ MySQL is installed"
else
    echo "❌ MySQL not found. Installing..."
    sudo apt update
    sudo apt install mysql-server -y
fi

# Check if MySQL is running
echo ""
echo "[2/6] Checking MySQL service..."
if sudo systemctl is-active --quiet mysql; then
    echo "✅ MySQL is running"
else
    echo "⚠️  MySQL is NOT running. Starting..."
    sudo systemctl start mysql
    sudo systemctl enable mysql
    sleep 3
    if sudo systemctl is-active --quiet mysql; then
        echo "✅ MySQL started successfully"
    else
        echo "❌ Failed to start MySQL"
        exit 1
    fi
fi

# Check current directory
echo ""
echo "[3/6] Checking project directory..."
if [ -f ".env" ]; then
    echo "✅ Found .env file"
    echo "Current DB configuration:"
    grep -E "^DB_" .env
else
    echo "⚠️  .env file not found in current directory"
    echo "Creating default .env..."
    cat > .env << 'EOF'
SECRET_KEY=supersecretkey123
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=earthquake_db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
EOF
    echo "✅ Created .env file"
fi

# Get DB credentials
echo ""
echo "[4/6] Reading database configuration..."
source .env
DB_HOST=${DB_HOST:-localhost}
DB_USER=${DB_USER:-root}
DB_NAME=${DB_NAME:-earthquake_db}

echo "DB_HOST: $DB_HOST"
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"

# Create database if it doesn't exist
echo ""
echo "[5/6] Setting up database..."
if [ "$DB_PASSWORD" = "" ]; then
    sudo mysql -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" 2>/dev/null
    sudo mysql -e "SHOW DATABASES;" | grep -q "$DB_NAME"
else
    mysql -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" 2>/dev/null
fi

if [ $? -eq 0 ]; then
    echo "✅ Database '$DB_NAME' is ready"
else
    echo "⚠️  Could not verify database (may need manual setup)"
fi

# Test connection
echo ""
echo "[6/6] Testing Python database connection..."
python3 << EOF
import sys
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import pymysql
    
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'earthquake_db'),
        connect_timeout=5
    )
    print("✅ SUCCESS: Database connection working!")
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"✅ MySQL version: {version[0]}")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    if tables:
        print(f"✅ Found {len(tables)} tables in database")
    else:
        print("⚠️  No tables found (database is empty)")
    conn.close()
    sys.exit(0)
except ImportError:
    print("❌ pymysql not installed")
    print("Run: pip install pymysql")
    sys.exit(1)
except Exception as e:
    print(f"❌ Connection FAILED: {e}")
    print("\nPossible fixes:")
    print("1. Check MySQL is running: sudo systemctl status mysql")
    print("2. Set DB password in .env file")
    print("3. Run: sudo mysql -e 'CREATE DATABASE earthquake_db;'")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ DATABASE CONNECTION FIXED!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Restart your Flask app"
    echo "2. Test: curl http://localhost:5000"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠️  NEEDS MANUAL ATTENTION"
    echo "=========================================="
    echo ""
    echo "Try these commands:"
    echo "  sudo systemctl status mysql"
    echo "  sudo mysql -u root -p"
    echo "  mysql -h localhost -u root -p"
fi

