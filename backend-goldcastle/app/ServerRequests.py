from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS  # Import CORS
import logging
import subprocess
import time
import random
import string

def start_electionChecker():
    try:
        subprocess.Popen(['python3', 'scripts/10_electionChecker.py'])
    except Exception as e:
        logging.exception("An error occurred while starting the external election Checker script:")

def start_overlordChecker():
        try:
            subprocess.Popen(['python3', 'scripts/1_checkOverlordAndPower.py'])
        except Exception as e:
            logging.exception("An error occurred while starting the external Overlord Checker script:")

# Set up logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

# Database connection parameters
db_params = {
    'dbname': 'goldcastle',
    'user': 'esse',
    'password': '96509035',
    'host': 'postgres',
    'port': '5432'
}

@app.route('/count_null_owners', methods=['GET'])
def count_null_owners():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to count rows where owner is NULL
        query = "SELECT COUNT(*) FROM nft_goldcastle_asia WHERE owner IS NOT NULL"

        # Execute the query
        cursor.execute(query)

        # Fetch the count
        count = cursor.fetchone()[0]

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return count of rows where owner is NULL
        return jsonify({'count_null_owners': count})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500



@app.route('/comparewarlords', methods=['POST'])
def compare_warlords():
    try:
        # Get the array from the request data
        data = request.json
        array = data.get('array')

        if not array:
            return jsonify({'error': 'Array not provided in request'}), 400

        # Convert array elements to strings
        array = [str(value) for value in array]

        logging.debug(f"Received array: {array}")

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query with correct number of placeholders
        query = "SELECT * FROM nft_goldcastle_asia WHERE nftcontractid = ANY(%s) AND members != 1 AND nftselfcontractaddress = overlord AND killed = False"

        # Execute the query with the array elements as parameters
        cursor.execute(query, (array,))

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500



@app.route('/compare', methods=['POST'])
def compare_values():
    try:
        # Get the array from the request data
        data = request.json
        array = data.get('array')

        if not array:
            return jsonify({'error': 'Array not provided in request'}), 400

        # Convert array elements to strings
        array = [str(value) for value in array]

        logging.debug(f"Received array: {array}")

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query with correct number of placeholders
        query = "SELECT * FROM nft_goldcastle_asia WHERE nftcontractid = ANY(%s)"

        # Execute the query with the array elements as parameters
        cursor.execute(query, (array,))

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/get_lordsubjectindex', methods=['GET'])
def get_lordsubjectindex():
    try:
        # Get lordaddress from the request parameters
        lordaddress = request.args.get('lordaddress')

        if not lordaddress:
            return jsonify({'error': 'Lord address not provided in request'}), 400

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query to select lordsubjectindex where lordaddress matches
        query = "SELECT lordsubjectindex FROM fealtycontracts WHERE lordaddress = %s AND (hasbeenaccepted IS NULL OR hasbeenaccepted = False)"

        # Execute the query with the lordaddress parameter
        cursor.execute(query, (lordaddress,))

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Extract lordsubjectindex values into an array
        lordsubjectindex_array = [row[0] for row in rows]

        return jsonify({'lordsubjectindex': lordsubjectindex_array})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/fealtycontracts/<int:page>')
def get_fealty_contracts(page):
    try:
        # Calculate the offset based on the page number
        offset = (page - 1) * 50

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to select 50 rows from fealtycontracts table with offset
        query = "SELECT * FROM fealtycontracts WHERE hasbeenaccepted IS NULL ORDER BY lordsubjectindex LIMIT 50 OFFSET %s"

        # Execute the query with the offset parameter
        cursor.execute(query, (offset,))

        # Fetch the rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Convert rows to list of dictionaries with column names as keys
        result = []
        for row in rows:
            row_dict = {}
            for column, value in zip([column[0] for column in cursor.description], row):
                # Replace None values with 0
                row_dict[column] = value if value is not None else 0
            result.append(row_dict)

        return jsonify(result)

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/marriagecontracts/<int:page>')
def get_marriage_contracts(page):
    try:
        # Calculate the offset based on the page number
        offset = (page - 1) * 50

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to select 50 rows from fealtycontracts table with offset
        query = "SELECT * FROM marriagecontracts WHERE hasbeenaccepted IS NULL OR hasbeenaccepted = false ORDER BY dowry LIMIT 50 OFFSET %s"

        # Execute the query with the offset parameter
        cursor.execute(query, (offset,))

        # Fetch the rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Convert rows to list of dictionaries with column names as keys
        result = []
        for row in rows:
            row_dict = {}
            for column, value in zip([column[0] for column in cursor.description], row):
                # Replace None values with 0
                row_dict[column] = value if value is not None else 0
            result.append(row_dict)

        return jsonify(result)

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/get_value', methods=['GET'])
def get_value():
    try:
        # Get parameters from the request
        nftselfcontractaddress = request.args.get('nftselfcontractaddress')
        selectortype = request.args.get('selectortype')

        if not nftselfcontractaddress or not selectortype:
            return jsonify({'error': 'Both nftselfcontractaddress and selectortype are required'}), 400

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query
        query = "SELECT {} FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s".format(selectortype)

        # Execute the query with the nftselfcontractaddress parameter
        cursor.execute(query, (nftselfcontractaddress,))

        # Fetch the value
        value = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        if value:
            return jsonify({selectortype: value[0]})
        else:
            return jsonify({'message': 'No value found for the provided nftselfcontractaddress and selectortype'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/top3wonamount')
def get_top3_won_amount():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to select the 3 biggest amounts from goldwithdraw table
        query = "SELECT wonamount, address, datetime FROM goldwithdraw ORDER BY wonamount DESC LIMIT 3"

        # Execute the query
        cursor.execute(query)

        # Fetch the rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Extract the amounts from the rows
        top3_data = []

        for row in rows:
            top3_data.append({
                'wonamount': row[0],
                'address': row[1],
                'datetime': row[2]  # Assuming datetime is in datetime format
            })

        return jsonify(top3_data)

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/goldtokenstate')
def get_highest_datetime_row():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to select the row with the highest datetime value
        query = "SELECT * FROM goldwithdraw ORDER BY datetime DESC LIMIT 1"

        # Execute the query
        cursor.execute(query)

        # Fetch the row
        row = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return the row
        return jsonify({
            'address': row[0],
            'wonamount': row[1],
            'datetime': row[2],
            'txid': row[3],
            'jackpot': row[4]
        })

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500



@app.route('/wars')
def get_wars():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query with correct number of placeholders
        query = "SELECT * FROM nft_goldcastle_asia WHERE members != 1 AND nftselfcontractaddress = overlord AND killed = False;"

        # Execute the query with the array elements as parameters
        cursor.execute(query)

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/overlords')
def get_data():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query with correct number of placeholders
        query = "SELECT * FROM nft_goldcastle_asia WHERE isoverlord = True AND members != 1;"

        # Execute the query with the array elements as parameters
        cursor.execute(query)

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/underlords')
def get_underlords():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query with correct number of placeholders
        query = "SELECT * FROM nft_goldcastle_asia WHERE members = 1 AND owner IS NOT NULL;"

        # Execute the query with the array elements as parameters
        cursor.execute(query)

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

def get_sworn_nfts(nft_self_contract_address, exclude_self=True):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Query the database for sworn NFTs, excluding the current NFT if exclude_self is True
    if exclude_self:
        cur.execute("SELECT * FROM nft_goldcastle_asia WHERE feudallord = %s::VARCHAR AND nftselfcontractaddress != %s::VARCHAR", (nft_self_contract_address, nft_self_contract_address,))
    else:
        cur.execute("SELECT * FROM nft_goldcastle_asia WHERE feudallord = %s::VARCHAR", (nft_self_contract_address,))

    sworn_nfts = cur.fetchall()

    # Close database connection
    cur.close()
    conn.close()

    # Recursive step: Get sworn NFTs of sworn NFTs
    sworn_nfts_data = []
    for nft in sworn_nfts:
        sworn_nft_self_contract_address = nft[0]  # Assuming the first column is the NFT self contract address
        sworn_nft_data = {
            "nft_self_contract_address": sworn_nft_self_contract_address,
        }
        # Include all column values in the sworn_nft_data dictionary
        for idx, column_name in enumerate(cur.description):
            column_value = nft[idx]
            sworn_nft_data[column_name.name] = column_value

        # Recursively fetch sworn NFTs
        sworn_nft_data["sworn_nfts"] = get_sworn_nfts(sworn_nft_self_contract_address, exclude_self=False)  # Excluding self for all subsequent calls

        sworn_nfts_data.append(sworn_nft_data)

    return sworn_nfts_data

# Flask route to handle requests for fetching NFT data
@app.route('/overlordmembers/<nft_self_contract_address>')
def get_nfts(nft_self_contract_address):
    # Call the recursive function to get hierarchical data
    logging.debug(f"Received array: {nft_self_contract_address}")

    nfts_data = get_sworn_nfts(nft_self_contract_address)
    logging.debug(f"Received array: {nfts_data}")
    return jsonify(nfts_data)


@app.route('/wartarget/<nft_contract_address>')
def get_wartarget_data(nft_contract_address):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query
        query = "SELECT * FROM nft_goldcastle_asia WHERE wartarget = %s AND nftselfcontractaddress != %s"

        # Execute the query with the NFT contract address as parameter
        cursor.execute(query, (nft_contract_address,nft_contract_address))

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found for the given NFT contract address'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500




@app.route('/anathemadeclarations/<nft_contract_address>')
def get_declarer_data(nft_contract_address):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query
        query = "SELECT * FROM anathemacontracts WHERE declareraddress = %s"

        # Execute the query with the NFT contract address as parameter
        cursor.execute(query, (nft_contract_address,))

        # Fetch the matching rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching rows as JSON response
        if rows:
            # Convert rows to list of dictionaries with column names as keys
            result = []
            for row in rows:
                row_dict = {}
                for column, value in zip([column[0] for column in cursor.description], row):
                    # Replace None values with 0
                    row_dict[column] = value if value is not None else 0
                result.append(row_dict)
            return jsonify(result)
        else:
            return jsonify({'message': 'No matching rows found for the given NFT contract address'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/singlenftdata/<nft_self_contract_address>')
def get_nft_data(nft_self_contract_address):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query
        query = "SELECT * FROM nft_goldcastle_asia WHERE nftselfcontractaddress = %s"

        # Execute the query with the NFT self contract address as parameter
        cursor.execute(query, (nft_self_contract_address,))

        # Fetch the matching row
        row = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching row as JSON response
        if row:
            # Convert row to a dictionary with column names as keys
            row_dict = {}
            for column, value in zip([column[0] for column in cursor.description], row):
                # Replace None values with 0
                row_dict[column] = value if value is not None else 0
            return jsonify(row_dict)
        else:
            return jsonify({'message': 'No matching row found for the given NFT self contract address'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/election/<int:election_id>')
def get_election_data(election_id):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the parameterized SQL query
        query = "SELECT * FROM election WHERE electionid = %s"

        # Execute the query with the electionid as parameter
        cursor.execute(query, (election_id,))

        # Fetch the matching row
        row = cursor.fetchone()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Return matching row as JSON response
        if row:
            # Convert row to a dictionary with column names as keys
            row_dict = {}
            for column, value in zip([column[0] for column in cursor.description], row):
                # Replace None values with 0
                row_dict[column] = value if value is not None else 0
            return jsonify(row_dict)
        else:
            return jsonify({'message': 'No matching row found for the given election ID'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/marketplacelistings/<int:page>')
def get_marketplace_listings(page):
    try:
        # Calculate the offset based on the page number
        offset = (page - 1) * 50

        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Construct the SQL query to select 50 rows from fealtycontracts table with offset
        query = "SELECT * FROM marketplacelistings WHERE bought IS NULL ORDER BY timelisted LIMIT 50 OFFSET %s"

        # Execute the query with the offset parameter
        cursor.execute(query, (offset,))

        # Fetch the rows
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        conn.close()

        # Convert rows to list of dictionaries with column names as keys
        result = []
        for row in rows:
            row_dict = {}
            for column, value in zip([column[0] for column in cursor.description], row):
                # Replace None values with 0
                row_dict[column] = value if value is not None else 0
            result.append(row_dict)

        return jsonify(result)

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

import subprocess

@app.route('/checkminting')
def start_checkminting():
    try:

        mjs_process = subprocess.Popen(['node', 'scripts/2_checkminting.mjs'])
        mjs_process.wait()
        time.sleep(3)
        start_overlordChecker()


        return jsonify({'message': 'Checkminting script started successfully'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/checkgoldcontract')
def start_checkgoldcontract():
    try:

        # Start the mjs script subprocess
        mjs_process = subprocess.Popen(['node', 'scripts/4_checkGoldContract.mjs'])
        # Wait for the mjs script subprocess to finish
        mjs_process.wait()


        mjs_process.wait()
        return jsonify({'message': 'checkgoldcontract script started successfully'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/checkfealtycontract')
def start_checkfealtycontract():
    try:
        mjs_process = subprocess.Popen(['node', 'scripts/3_checkFealtyContractsState.mjs'])
        mjs_process.wait()
        start_overlordChecker()

        return jsonify({'message': 'checkfealtycontract script started successfully'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500

@app.route('/checkfealtycontractandelection')
def start_checkfealtycontractandelection():
    try:
        mjs_process = subprocess.Popen(['node', 'scripts/3_checkFealtyContractsState.mjs'])
        mjs_process.wait()
        start_overlordChecker()
        start_electionChecker()

        return jsonify({'message': 'checkfealtycontract script started successfully'})

    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


def checkingDatabase():
    i = 15
    while True:
        try:
            # Replace the function call below with the function you want to continuously run
            # For example: start_checkfealtycontract()
            print("Running database checks...")

            mjs_process = subprocess.Popen(['node', 'scripts/2_checkminting.mjs'])
            mjs_process = subprocess.Popen(['node', 'scripts/3_checkFealtyContractsState.mjs'])
            mjs_process = subprocess.Popen(['node', 'scripts/4_checkGoldContract.mjs'])
            mjs_process = subprocess.Popen(['node', 'scripts/8_checkMarketplace.mjs'])

            mjs_process.wait()
            start_overlordChecker()
            start_electionChecker()
            # Wait for a few minutes before running the function again
            time.sleep(120)
            i += 1
            if i == 15:
                mjs_process = subprocess.Popen(['node', 'scripts/5_databaseAddingFromContractState.mjs'])
                i = 0

        except Exception as e:
            logging.exception("An error occurred during continuous function run:")

@app.route('/checkingDatabase')
def start_checkingDatabase():
    try:
        # Start the continuous function in a separate thread
        from threading import Thread
        thread = Thread(target=checkingDatabase)
        thread.start()

        return jsonify({'message': 'Continuous function started successfully'})
    except Exception as e:
        logging.exception("An error occurred:")
        return jsonify({'error': str(e)}), 500


@app.route('/verifydiscord', methods=['POST'])
def verify():
    # Extract data from request body
    data = request.get_json()
    address = data.get('address')
    publicKey = data.get('publicKey')
    discordid = data.get('discordid')

    # Concatenate address, publicKey, and discordname
    combined_data = address + publicKey + discordid

    # Generate randomized string based on combined_data
    randomized_string = ''.join(random.choices(combined_data, k=10))

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    query = "INSERT INTO owners (address, publickey, discordid, message) VALUES (%s, %s, %s, %s)"

    # Execute the query with the offset parameter
    cursor.execute(query, (address, publicKey, discordid, randomized_string,))
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    # Return randomized string as JSON response
    return jsonify({"message": randomized_string})


@app.route('/getdiscordroles', methods=['POST'])
def getdiscordroles():
    # Extract data from request body
    data = request.get_json()
    publicKey = data.get('publicKey')
    signature = data.get('signature')
    message = data.get('message')
    # Run the .mjs file with the provided arguments
    mjs_process = subprocess.Popen(['node', 'scripts/11_check_signature.mjs', publicKey, signature, message])
    mjs_process.wait()
    
    return '', 204  # Return an empty response with a 204 status code


if __name__ == '__main__':
    app.run(debug=True, port=4000)
