import psycopg2
from psycopg2 import sql
import datetime



db_params = {
    'dbname': 'goldcastle',
    'user': 'esse',
    'password': '96509035',
    'host': 'postgres',
    'port': '5432'
}



def copy_postgres_databases():
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect(**db_params)

 
        conn.autocommit = True
        cursor = conn.cursor()

        # Get a list of databases
        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()

        # Delete copies from two days before
        two_days_ago = datetime.now() - datetime.timedelta(days=2)
        for db in databases:
            db_name = db[0]
            copy_name = f"{db_name}_copy"
            copy_name_two_days_ago = f"{db_name}_copy_{two_days_ago.strftime('%Y%m%d')}"
            cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(
                sql.Identifier(copy_name_two_days_ago)
            ))

        # Create copies of the databases
        for db in databases:
            db_name = db[0]
            copy_name = f"{db_name}_copy_{datetime.now().strftime('%Y%m%d')}"
            cursor.execute(sql.SQL("CREATE DATABASE {} TEMPLATE {};").format(
                sql.Identifier(copy_name),
                sql.Identifier(db_name)
            ))

        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print("An error occurred during database copy:", e)
        return False
    
copy_postgres_databases()