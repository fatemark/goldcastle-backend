import psycopg2
from psycopg2 import extras
import time

# Database connection configuration
conn = psycopg2.connect(
    user="esse",
    password="96509035",
    host="postgres",
    port="5432",
    database="goldcastle"
)

def main():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        # Retrieve rows where rarity is NULL
        cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE isoverlord IS True")
        rows = cursor.fetchall()

        option = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7:0}

        electiondeadline = 1.710327505*(10**12)
        electionstarted = 1709463505000
        electionname = 'Standing for consul'
        electionquestion = 'Should all classes be able to run for the office of consul?'
        
        # Generate a unique electionid
        electionid = 0

        for row in rows:
            if row['votetime'] < electiondeadline and row['votetime'] > electionstarted:
                option[row['vote']] += row['votingpower']

        # Construct the SQL query with ON CONFLICT clause
        sql_query = """
            INSERT INTO election (electionid, option0, option1, option2, option3, option4, option5, option6, option7, electionname, electiondeadline, electionstarted, electionquestion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (electionid) DO UPDATE 
            SET 
                option0 = EXCLUDED.option0,
                option1 = EXCLUDED.option1,
                option2 = EXCLUDED.option2,
                option3 = EXCLUDED.option3,
                option4 = EXCLUDED.option4,
                option5 = EXCLUDED.option5,
                option6 = EXCLUDED.option6,
                option7 = EXCLUDED.option7,
                electionname = EXCLUDED.electionname,
                electiondeadline = EXCLUDED.electiondeadline,
                electionstarted = EXCLUDED.electionstarted,
                electionquestion = EXCLUDED.electionquestion;
        """

        # Execute the SQL query with parameters
        cursor.execute(sql_query, (electionid, option[0], option[1], option[2], option[3], option[4], option[5], option[6], option[7], electionname, electiondeadline, electionstarted, electionquestion))

        # Commit the transaction
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error occurred:", error)

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()


# Call the main function
if __name__ == "__main__":
    main()
