import pymysql
from flask import current_app

def get_db():
    """
    Get database connection for local MySQL on Azure Ubuntu VM
    Configured for local MySQL instance (no SSL required)
    """
    try:
        connection = pymysql.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            db=current_app.config["DB_NAME"],
            port=current_app.config["DB_PORT"],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10,
            # Local MySQL configuration (no SSL)
            ssl=None,
            autocommit=False
        )
        return connection
    except pymysql.err.OperationalError as e:
        error_code, error_msg = e.args if isinstance(e.args, tuple) and len(e.args) > 1 else (None, str(e))
        if error_code == 1698:
            # Error 1698: Access denied - typically authentication plugin issue in MySQL 8.0+
            current_app.logger.error(
                f"MySQL Authentication Error (1698): {error_msg}\n"
                f"This usually happens with MySQL 8.0+ when user uses caching_sha2_password.\n"
                f"Solution: ALTER USER '{current_app.config['DB_USER']}'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';"
            )
        elif error_code == 2003:
            # Error 2003: Can't connect to MySQL server
            current_app.logger.error(
                f"MySQL Connection Error (2003): {error_msg}\n"
                f"Cannot connect to MySQL server at {current_app.config['DB_HOST']}:{current_app.config['DB_PORT']}\n"
                f"Ensure MySQL is running and accessible."
            )
        elif error_code == 1045:
            # Error 1045: Access denied
            current_app.logger.error(
                f"MySQL Access Denied (1045): {error_msg}\n"
                f"Check your DB_USER and DB_PASSWORD in .env file."
            )
        else:
            current_app.logger.error(f"MySQL Connection Error: {error_msg}")
        raise
    except Exception as e:
        current_app.logger.error(f"Unexpected database connection error: {str(e)}")
        raise
