import psycopg2
from psycopg2 import extras
from geopy.geocoders import Nominatim
import certifi
import urllib3
import os
import googlemaps
google_api_key = "AIzaSyCXEudEGLQvVmFM1MaykUKIDRfcABhAZPk"
gmaps = googlemaps.Client(key=google_api_key)

os.environ['SSL_CERT_FILE'] = certifi.where()

# Disable SSL verification
urllib3.disable_warnings()

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
        cursor.execute("SELECT * FROM nft_goldcastle_asia WHERE acoordinates IS NULL ORDER BY nftindex ASC")
        rows = cursor.fetchall()



        # Iterate through each row
        for row in rows:
            print(row['nftindex'])
            # Get coordinates for a place name
            if row['subdomain'] == '' or row['subdomain'] == None:
                location = gmaps.geocode(row['domain'])
            else:
                location = gmaps.geocode(row['subdomain'])


            cursor.execute("SELECT * FROM nft_goldcastle_asia")
            rows = cursor.fetchall() 
            # Print latitude and longitude
            # Get the first result from the list

            if location:
                first_result = location[0]
                xcoordinates = first_result['geometry']['location']['lng']
                ycoordinates = first_result['geometry']['location']['lat']
                print((row['subdomain'], xcoordinates, ycoordinates))
            else:
                xcoordinates = 0
                ycoordinates = 0
                print("No location: ", row['subdomain'])


            if row['continent'] == 'Asia':
                zcoordinates = 0
                acoordinates = 0
            else:
                if row['continent'] == 'Second Garden':
                    zcoordinates = 1000
                    acoordinates = 0
                elif row['continent'] == 'Fourth Dimension':
                    acoordinates = 1000
                    zcoordinates = 0
            cursor.execute("UPDATE nft_goldcastle_asia SET xcoordinates = %s, Ycoordinates = %s, Zcoordinates = %s, acoordinates = %s WHERE nftselfcontractaddress = %s", (xcoordinates, ycoordinates, zcoordinates, acoordinates, row['nftselfcontractaddress']))
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
