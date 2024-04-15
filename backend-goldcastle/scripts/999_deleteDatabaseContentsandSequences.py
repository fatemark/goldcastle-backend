import psycopg2
from psycopg2 import Error

def delete_all_records(table_name):
    try:
        # Connect to your PostgreSQL database
        connection = psycopg2.connect(
            user="esse",
            password="96509035",
            host="localhost",
            port="5432",
            database="goldcastle"
        )

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Define the table from which you want to delete all records

        # Construct the SQL DELETE statement
        delete_query = f"DELETE FROM {table_name};"
        sequencedeletequery = "ALTER SEQUENCE main_nft_index_sequence RESTART WITH 0;"
        # Execute the DELETE statement
        cursor.execute(delete_query)
        cursor.execute(sequencedeletequery)

        # Commit the changes to the database
        connection.commit()

        # Close the cursor and the connection
        cursor.close()
        connection.close()

        print("All records deleted successfully.")

    except (Exception, Error) as error:
        print("Error while deleting records from PostgreSQL", error)





if __name__ == "__main__":
    delete_all_records('nft_minting_goldcastle_asia')
    delete_all_records('nft_goldcastle_asia')
    delete_all_records('fealtycontracts')
    delete_all_records('goldtokencontracts')
    delete_all_records('goldwithdraw')
    delete_all_records('jackpotwinners')
    delete_all_records('marriagecontracts')
    delete_all_records('anathemacontracts')
    delete_all_records('marketplacelistings')
    delete_all_records('eventlisteningcheck')
    delete_all_records('minteventlisteningcheck')
    delete_all_records('marketplaceeventlisteningcheck')
    delete_all_records('goldcastleeventlisteningcheck')

    