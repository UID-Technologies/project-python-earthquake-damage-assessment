"""
Test Database Connection Script
Verifies connection to the configured database
"""
import pymysql
from app.config import Config

def test_database_connection():
    print("="*70)
    print("  DATABASE CONNECTION TEST")
    print("="*70)
    
    print("\nConfiguration:")
    print(f"  DB_HOST: {Config.DB_HOST}")
    print(f"  DB_USER: {Config.DB_USER}")
    print(f"  DB_NAME: {Config.DB_NAME}")
    print(f"  DB_PORT: {Config.DB_PORT}")
    
    print("\nAttempting connection...")
    
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            db=Config.DB_NAME,
            port=Config.DB_PORT,
            charset='utf8mb4',
            connect_timeout=10
        )
        
        print("[SUCCESS] Connected to database!")
        
        # Test a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"\nMySQL Version: {version[0]}")
            
            # Check if users table exists
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"\nTables found: {len(tables)}")
            
            # Check for key tables
            table_names = [table[0] for table in tables]
            required_tables = ['users', 'insurance', 'claims']
            
            print("\nChecking required tables:")
            for table in required_tables:
                if table in table_names:
                    print(f"  [OK] {table}")
                else:
                    print(f"  [MISSING] {table}")
        
        connection.close()
        print("\n[SUCCESS] Database connection test completed!")
        return True
        
    except pymysql.Error as e:
        print(f"\n[ERROR] Failed to connect to database!")
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] Unexpected error!")
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    success = test_database_connection()
    print("\n" + "="*70)
    if success:
        print("  Status: READY TO USE")
    else:
        print("  Status: CONNECTION FAILED")
    print("="*70)

