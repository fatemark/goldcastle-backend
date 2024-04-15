import psycopg2

def load_dump_to_database(dump_file, database, user, password, host, port):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        print("Connected to the database.")

        # Open the dump file and execute its contents line by line
        with open(dump_file, 'r') as f:
            cursor = conn.cursor()
            command = ""
            for line in f:
                if line.strip() == "" or line.strip().startswith("--") or line.strip().startswith("\\"):
                    continue  # Skip empty lines, comments, and meta-commands
                command += line
                if ";" in line:
                    try:
                        cursor.execute(command)
                    except psycopg2.Error as e:
                        print(f"Error executing command: {command.strip()}")
                        print(e)
                    command = ""
            conn.commit()
            cursor.close()

        print("Dump file loaded into the database successfully.")

    except psycopg2.Error as e:
        print("Error: Unable to connect to the database.")
        print(e)

    finally:
        if conn is not None:
            conn.close()
            print("Connection to the database closed.")

if __name__ == "__main__":
    # Specify the connection details
    user = "esse"
    password = "96509035"
    host = "localhost"
    port = "5432"
    database = "goldcastle"

    # Specify the path to the dump file
    dump_file = "/Users/esse/Desktop/crypto/gold_castle/databasebackups/databasebackups/db_backup_2024-03-08_10-11-17.sql"

    # Call the function to load the dump file into the database
    load_dump_to_database(dump_file, database, user, password, host, port)
