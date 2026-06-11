import os
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "placement_portal"),
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="placement_pool",
    pool_size=5,
    **DB_CONFIG,
)


def get_connection():
    return connection_pool.get_connection()
