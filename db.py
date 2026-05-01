import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Saiarun@123",
            database="face_attendance"
        )

        if conn.is_connected():
            print("✅ Connected to MySQL")
            return conn

    except Error as e:
        print("❌ Error:", e)
        return None


# ✅ TEST BLOCK (this is what you should use)
if __name__ == "__main__":
    conn = get_connection()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")

        print("📦 Tables in DB:")
        for table in cursor.fetchall():
            print("➡️", table[0])

        cursor.close()
        conn.close()