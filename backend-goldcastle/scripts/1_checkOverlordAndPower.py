import psycopg2
from psycopg2 import extras

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
        cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE rarity = 0")
        rows = cursor.fetchall()

        # Iterate through each row
        for row in rows:
            maxpowerpotential = 0
            members = 1
            vassals = 0
            # If ismarried is TRUE, calculate maxpowerpotential based on potentialmarriage
            if row['ismarried']:
                cursor.execute("SELECT potentialmarriage FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['nftselfcontractaddress'],))
                marriagepartner = cursor.fetchone()['potentialmarriage']
                cursor.execute("SELECT magic FROM nft_goldcastle_asia WHERE potentialmarriage = %s", (marriagepartner,))
                magic = cursor.fetchone()['magic']
                if magic:
                    maxpowerpotential = row['ap'] * (1 + (magic / 10))
                    maxdefensivepower = row['hp'] * (1 + (magic / 10))
                else:
                    maxpowerpotential = row['ap']
                    maxdefensivepower = row['hp']
                votingpower = 1
            else:
                # If ismarried is FALSE, set magic to 0
                maxpowerpotential = row['ap']
                maxdefensivepower = row['hp']
                votingpower = 1

            # Update the row with the calculated maxpowerpotential
            cursor.execute("UPDATE nft_goldcastle_asia SET maxpowerpotential = %s, maxdefensivepower = %s, votingpower = %s, members = %s, vassals = %s WHERE nftselfcontractaddress = %s", (maxpowerpotential, maxdefensivepower, votingpower, members, vassals, row['nftselfcontractaddress']))
            conn.commit()
        
        print(f"Data updated successfully for rarity NULL (0)")

        for i in range(1, 14):
            # Retrieve rows where rarity is 1
            cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE rarity = %s", (i,))
            rows = cursor.fetchall()
            # Iterate through each row
            for row in rows:
                cursor.execute("SELECT stars, maxpowerpotential, maxdefensivepower, votingpower, lives, wisdom, members FROM nft_goldcastle_asia WHERE feudallord = %s AND nftselfcontractaddress != %s", (row['nftselfcontractaddress'], row['nftselfcontractaddress']))
                subjects = cursor.fetchall()
                members = 1
                totalsubjectvotingpower = 0
                totalsubjectpotential = 0
                totalsubjectdefensepower = 0
                vassals = 0
                # Calculate subject potential and total subject potential
                for subject in subjects:
                    if subject['wisdom'] > 0:
                        wisdom = int(subject['wisdom']) / 10
                    else:
                        wisdom = int(subject['wisdom']) / 2000
                    if subject['stars']:
                        subjectpotential = subject['maxpowerpotential'] * (1 + subject['stars'] / 5) + wisdom
                        subjectdefensivepower = subject['maxdefensivepower'] * (1 + subject['lives'] / 10) + wisdom
                        subjectvotingpower = subject['votingpower']
                    else:
                        subjectpotential = subject['maxpowerpotential'] * 1 + wisdom
                        subjectdefensivepower = subject['maxdefensivepower'] * (1 + subject['lives'] / 10) + wisdom
                        subjectvotingpower = subject['votingpower']
                    totalsubjectpotential += subjectpotential
                    totalsubjectdefensepower += subjectdefensivepower
                    totalsubjectvotingpower += subjectvotingpower
                    members += subject['members']
                    vassals += 1
                # If ismarried is TRUE, calculate maxpowerpotential based on potentialmarriage
                cursor.execute("SELECT potentialmarriage FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['nftselfcontractaddress'],))
                marriagepartner = cursor.fetchone()['potentialmarriage']


                if marriagepartner != row['nftselfcontractaddress']:
                    if row['nftindex'] == 87:
                         print(row['nftindex'])
                    magic = 0
                    cursor.execute("SELECT magic FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s ", (marriagepartner,))
                    partnermagic = cursor.fetchone()['magic']
                    magic += partnermagic
                    maxpowerpotential = row['ap'] * (1 + (magic / 10)) + totalsubjectpotential * (1 + row['rarity'] / 10)
                    maxdefensivepower = row['hp'] * (1 + (magic / 10)) + totalsubjectdefensepower * (1 + row['rarity'] / 10)
                else:
                    maxpowerpotential = row['ap'] + totalsubjectpotential * (1 + row['rarity'] / 10)
                    maxdefensivepower = row['hp'] + totalsubjectdefensepower * (1 + row['rarity'] / 10)  


                votingpower = row['rarity'] + 1 + (1 + row['rarity'] / 10) * totalsubjectvotingpower

                # Update the row with the calculated maxpowerpotential
                cursor.execute("UPDATE nft_goldcastle_asia SET maxpowerpotential = %s, maxdefensivepower = %s, votingpower = %s, members = %s, vassals = %s WHERE nftselfcontractaddress = %s", (maxpowerpotential, maxdefensivepower, votingpower, members, vassals, row['nftselfcontractaddress']))
                conn.commit()
            print(f"Data updated successfully for rarity {i}")


        cursor.execute("UPDATE nft_goldcastle_asia SET isoverlord = NULL;")
        conn.commit()
        cursor.execute("SELECT * FROM nft_goldcastle_asia")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("UPDATE nft_goldcastle_asia SET overlord = %s, isoverlord = True WHERE feudallord = %s AND feudallord = nftselfcontractaddress", (row['nftselfcontractaddress'], row['nftselfcontractaddress']))
            conn.commit()

        


        def find_overlord(feudallord):
            """Function to find the overlord for a given feudallord"""
            cursor.execute("SELECT overlord FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (feudallord,))
            overlord = cursor.fetchone()
            if overlord:
                return overlord[0]
            else:
                return None  # Return None if overlord not found

        cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE isoverlord IS NOT TRUE")
        underlords = cursor.fetchall()

        for i in range(14, -1, -1):
            if i != 0:
                cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE isoverlord IS NOT TRUE AND rarity = %s", (i,))
            else:
                cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE isoverlord IS NOT TRUE AND rarity = 0")
            underlords = cursor.fetchall()

            # Update overlord for each underlord
            for underlord in underlords:
                overlord = find_overlord(underlord['feudallord'])
                
                if overlord is not None:
                    cursor.execute("UPDATE nft_goldcastle_asia SET overlord = %s, isoverlord = False WHERE feudallord = %s and nftselfcontractaddress = %s", (overlord, underlord['feudallord'], underlord['nftselfcontractaddress']))
                    conn.commit()

        def update_wives():
            # Select all rows where potentialmarriage is not equal to nftselfcontractaddress
            cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress != potentialmarriage")
            rows = cursor.fetchall()

            for row in rows:
                # Check if the potentialmarriage of the current row is equal to nftselfcontractaddress of any other row
                cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['potentialmarriage'],))
                second_row = cursor.fetchone()

                if second_row and second_row['potentialmarriage'] == row['nftselfcontractaddress']:
                    # If the condition is met, update the wife column of the first row
                    cursor.execute("UPDATE nft_goldcastle_asia SET wife = %s, potentialmarriage = %s, wifeallegiance = %s WHERE nftselfcontractaddress = %s", (second_row['name'], second_row['nftselfcontractaddress'], second_row['allegiance'], row['nftselfcontractaddress']))

            conn.commit()
        cursor.execute("UPDATE nft_goldcastle_asia SET wife = %s WHERE potentialmarriage = nftselfcontractaddress", ('Unmarried',))
        conn.commit()


        def update_wars():
            # Select all rows where potentialmarriage is not equal to nftselfcontractaddress
            cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE wartarget != nftselfcontractaddress")
            rows = cursor.fetchall()

            for row in rows:
                # Check if the potentialmarriage of the current row is equal to nftselfcontractaddress of any other row
                cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['wartarget'],))
                second_row = cursor.fetchone()

                cursor.execute("UPDATE nft_goldcastle_asia SET wartargetname = %s WHERE nftselfcontractaddress = %s", (second_row['name'], row['nftselfcontractaddress']))

            conn.commit()
        cursor.execute("UPDATE nft_goldcastle_asia SET wartargetname = %s WHERE wartarget = nftselfcontractaddress", ('N.A.',))
        conn.commit()


        def update_overlords():
            cursor.execute("SELECT nftselfcontractaddress, overlord FROM nft_goldcastle_asia")
            rows = cursor.fetchall()

            for row in rows:
                cursor.execute("SELECT name, rarity, nfturi, allegiance FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['overlord'],))
                second_row = cursor.fetchone()

                if second_row:
                    cursor.execute("UPDATE nft_goldcastle_asia SET overlordname = %s, overlordrarity = %s, overlordnfturi = %s, overlordallegiance = %s WHERE nftselfcontractaddress = %s", (second_row['name'], second_row['rarity'], second_row['nfturi'], second_row['allegiance'], row['nftselfcontractaddress']))

            conn.commit()


        def update_feudallord():
            cursor.execute("SELECT nftselfcontractaddress, feudallord FROM nft_goldcastle_asia")
            rows = cursor.fetchall()

            for row in rows:
                cursor.execute("SELECT name FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s", (row['feudallord'],))
                second_row = cursor.fetchone()

                if second_row:
                    cursor.execute("UPDATE nft_goldcastle_asia SET feudallordname = %s WHERE nftselfcontractaddress = %s", (second_row['name'], row['nftselfcontractaddress']))

            conn.commit()



        # Call the update_wives function
        update_wives()
        update_wars()
        update_overlords()
        update_feudallord()
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

