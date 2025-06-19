import psycopg
from psycopg.errors import Error
import dotenv
import os

dotenv.load_dotenv()

def restore_sql_file(sql_file_path, db_name, user, password, host="localhost", port="5432"):
    try:
        with psycopg.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            autocommit=True
        ) as conn: 
            print("Creating db")
            conn.execute("DROP DATABASE IF EXISTS project;")
            conn.execute("CREATE DATABASE project;")
        # Read the entire SQL file
        with open(sql_file_path, "r", encoding="latin1") as f:
            sql_script = f.read()

        # Connect to the database
        with psycopg.connect(
            dbname=db_name,
            user=user,
            password=password,
            host=host,
            port=port
        ) as conn:
           
            # Execute each statement safely
            with conn.cursor() as cur:
                for statement in sql_script.split(';'):
                    stmt = statement.strip()
                    if stmt:
                        cur.execute(stmt + ';')

            print("Database restored successfully.")

    except Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"General error: {e}")

# Example usage
if __name__ == "__main__":
    restore_sql_file(
        sql_file_path="backup.sql",
        db_name="project",
        user=os.getenv("SQL_USER"),
        password=os.getenv("SQL_PASSWORD")
    )
