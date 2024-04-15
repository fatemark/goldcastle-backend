import psycopg2
from psycopg2 import extras
import urllib3


# Database connection configuration
conn = psycopg2.connect(
    user="esse",
    password="96509035",
    host="localhost",
    port="5432",
    database="goldcastle"
)

def main():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    try:
        # Retrieve rows where rarity is NULL
        cursor.execute("SELECT * FROM nft_goldcastle_asia ORDER BY nftindex ASC")
        rows = cursor.fetchall()



        # Iterate through each row
        for row in rows:
            

            lives = row['lives']
            warattack = row['maxpowerpotential']
            warhp = row['maxdefensivepower']
            healing = 0

            if row['potentialmarriage'] != row['nftselfcontractaddress']:
                query = f"SELECT magic FROM nft_goldcastle_asia WHERE nftselfcontractaddress = '{row['potentialmarriage']}'"
                cursor.execute(query)                
                magic_result = cursor.fetchone()
                if magic_result[0] != None:
                    healing = magic_result[0] + row['magic']
                else:
                    healing = row['magic']
            else:
                healing = row['magic']



            cursor.execute("UPDATE nft_goldcastle_asia SET killed = False, warlives = %s, kills = %s, healing = %s, warattack = %s, warhp = %s WHERE nftselfcontractaddress = %s", (lives, 0, healing, warattack, warhp, row['nftselfcontractaddress']))
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
