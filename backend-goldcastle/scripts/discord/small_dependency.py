import json
import subprocess
import asyncio
import os


def numberresult(num):
    result = ""
    x = [int(digit) for digit in str(num)]
    for digit in x:
        if digit == 0:
            result += ":zero:"
        if digit == 1:
            result += ":one:"
        if digit == 2:
            result += ":two:"
        if digit == 3:
            result += ":three:"
        if digit == 4:
            result += ":four:"
        if digit == 5:
            result += ":five:"
        if digit == 6:
            result += ":six:"
        if digit == 7:
            result += ":seven:"
        if digit == 8:
            result += ":eight:"
        if digit == 9:
            result += ":nine:"
    print(result)


def getNftNameCount(count):
    result = "NFTs"
    if count == 1:
        result = "NFT"
    return result

def get_token_name(token_id):
    json_file = os.path.join(os.path.dirname(__file__), 'jsondata', 'tokenlist.json')
    name = "Unverified"
    symbol = "Unverified"
    with open(json_file, 'r') as f:
        data = json.load(f)
        
        for token in data['tokens']:
            if token['id'] == token_id:
                name = token['name']
                symbol= token['symbol']

    return symbol

def get_collection_name(collection_address):
    json_file = os.path.join(os.path.dirname(__file__), 'jsondata', 'collections.json')
    
    # Check if the JSON file exists
    if os.path.exists(json_file):
        # Read the JSON file
        with open(json_file, 'r') as file:
            data = json.load(file)
            collections = data.get('collections', [])
            
            # Check if there is an entry for the given address
            for collection in collections:
                if collection.get('address') == collection_address:
                    collection_name = collection.get('name')
                    print("Collection Name (from JSON):", collection_name)
                    return collection_name
    
    script_path = os.path.join(os.path.dirname(__file__), 'nodescripts', 'collection_name.mjs')
    
    try:
        output = subprocess.check_output(['node', script_path, collection_address], universal_newlines=True)
        collection_name = output.strip()
        return collection_name
    except subprocess.CalledProcessError as e:
        print("Error running the script:", e)
        return None


def getguilds():
    guilds = []
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())
            guilds.append(config_array[0])

    print(guilds)
    return guilds

def getroleschannel(guild):
    roleschannel = ""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())

            if config_array[0] == guild:
                roleschannel = config_array[5]

    return roleschannel


def getverificationchannel(guild):
    verifchannel = ""
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())

            if config_array[0] == guild:
                verifchannel = config_array[6]

    return verifchannel



def get_deletion_exclusion(guild):
    delete_expired = False
    exclusions = []

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())

            if config_array[0] == guild:
                delete_expired = config_array[7]
                exclusions = config_array[8]

    return delete_expired, exclusions


def get_bot_username(guildid):
    username = "Rosy"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())

            if config_array[0] == guildid:
                username = config_array[9]

    return username




def get_bot_avatar(guildid):
    avatar = ""

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    file_path = os.path.join(script_dir, "rosy/guild_configs/guilds_rosy.json")

    with open(file_path, 'r') as file:
        json_data = json.load(file)

    configurations = json_data["configuration"]

    configurations_length = len(configurations)
    print(configurations_length)

    if configurations_length > 0:
        for config in configurations:
            config_array = list(config.values())

            if config_array[0] == guildid:
                avatar = config_array[10]

    return avatar





def remove_quotes_if_present(input_string):
    if input_string.startswith('"') and input_string.endswith('"'):
        return input_string[1:-1]  # Remove the first and last characters (quotes)
    elif input_string.startswith("'") and input_string.endswith("'"):
        return input_string[1:-1]  # Remove the first and last characters (quotes)
    else:
        return input_string  # Return the string as it is if it's not enclosed in quotes
