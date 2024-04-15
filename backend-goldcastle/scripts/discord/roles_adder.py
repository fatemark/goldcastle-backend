import discord
import psycopg2
from discord.ext import commands, tasks
import asyncio
import os
from audio import elevenlabs
import random
from deleteaudio import delete_audio_files
import json
from small_dependency import numberresult, get_token_name, get_collection_name, getNftNameCount
import numpy as np

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Database connection details
db_config = {
    'host': 'postgres',
    'database': 'goldcastle',
    'user': 'esse',
    'password': '96509035'
}

def get_db_connection():
    return psycopg2.connect(**db_config)


def tokenroles(guild_id, discord_id):
    token_roles_list = []
    nft_count_roles_list = []
    nft_trait_roles_list = []
    all_role_ids = []

    role_ids_to_add = []
    try:
        # Get the directory of the currently executing script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the relative path to the JSON file
        file_path = os.path.join(script_dir, f"rosy/guild_configs/guild_{guild_id}.json")

        with open(file_path, 'r') as file:
            json_data = json.load(file)
            
    
        token_roles = json_data.get("TOKEN_ROLES", {})
        token_roles_length = len(token_roles)
        token_roles_list = list(token_roles.items())


        nft_count_roles = json_data.get("NFT_COUNT_ROLES", {})
        nft_count_roles_length = len(nft_count_roles)
        nft_count_roles_list = list(nft_count_roles.items())

        nft_trait_roles = json_data.get("NFT_TRAIT_ROLES", {})
        nft_trait_roles_length = len(nft_trait_roles)
        nft_trait_roles_list = list(nft_trait_roles.items())

    except Exception as e:
        print(f"Cannot add roles for tokens: {e}")

    
    try:
        token_roles_length -= 1
        while(token_roles_length >= 0):
            tokenid = token_roles_list[token_roles_length][0]
            symbol = get_token_name(tokenid)

            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = %s AND column_name = %s)", ('goldowners', symbol))
                    exists = cur.fetchone()[0]
                    if not exists:
                        sql_query = f'ALTER TABLE goldowners ADD COLUMN "{symbol}" VARCHAR(255)'
                        cur.execute(sql_query)
                        conn.commit()
            except Exception as e:
                print("Failed to make database:", e)

            rolesfortoken = len(token_roles_list[token_roles_length][1])
            n = rolesfortoken - 1
            while(n >= 0):
                print(token_roles_list[token_roles_length][n])
                amount = token_roles_list[token_roles_length][1][n][0]
                roleid = token_roles_list[token_roles_length][1][n][1]

                all_role_ids.append(roleid)

                conn = get_db_connection()
                try:
                    with conn.cursor() as cur:
                        cur.execute(f'SELECT "{symbol}" FROM goldowners WHERE discordid = {discord_id}')
                        result = cur.fetchone()
                        token_balance = result[0] if result else 0
                except:
                    print("Couldn't query the database")

                try:
                    if token_balance > amount:
                        role_ids_to_add.append(roleid)
                        print(f"Added role {roleid} for {symbol}")
                except:
                    print("Could not compare amounts")
                n -= 1



            token_roles_length -= 1
    except:
        print("Could not add tokenrules")    
    


    try:
        ######## nft counts :
        print(nft_count_roles_length)
        nft_count_roles_length -= 1

        while nft_count_roles_length >= 0:
            collectionaddress = nft_count_roles_list[nft_count_roles_length][0]


            rolecount = len(nft_count_roles_list[nft_count_roles_length][1])
            rolecount -= 1
            while rolecount >= 0:
                # nftamount = nft_count_roles_list[nft_count_roles_length][1][collectioncount]
                nftcount_rolid = nft_count_roles_list[nft_count_roles_length][1][rolecount][1]
                amount = nft_count_roles_list[nft_count_roles_length][1][rolecount][0]

                all_role_ids.append(nftcount_rolid)

                nft_balance = 0
                conn = get_db_connection()
                try:
                    with conn.cursor() as cur:
                        cur.execute("SELECT COUNT(*) FROM allnfts WHERE discordid = %s AND collectionaddress = %s", (discord_id, collectionaddress))
                        result = cur.fetchone()
                        nft_balance = result[0] if result else 0
                        print(nft_balance)
                except Exception as e:
                    print(f"Couldn't query the database: {str(e)}")

                if nft_balance >= amount:
                    role_ids_to_add.append(nftcount_rolid)
                    print(f"Added role {nftcount_rolid} for {get_collection_name(collectionaddress)}")
                else:
                    print(f"Not enough NFTs of for {get_collection_name(collectionaddress)}")


                rolecount -= 1


            nft_count_roles_length -= 1
    except:
        print("Could not process NFT count rules")





    try:
        ###### nft traits
        print(nft_trait_roles_length)
        nft_trait_roles_length -= 1

        while nft_trait_roles_length >= 0:
            collectionaddress = nft_trait_roles_list[nft_trait_roles_length][0]


            rolecount = len(nft_trait_roles_list[nft_trait_roles_length][1])
            
            rolecount -= 1
            while rolecount >= 0:

                print(nft_trait_roles_list[nft_trait_roles_length][1][rolecount])
                nft_trait_type = nft_trait_roles_list[nft_trait_roles_length][1][rolecount][0]
                nft_trait_value = nft_trait_roles_list[nft_trait_roles_length][1][rolecount][1]
                nfttrait_roleid = nft_trait_roles_list[nft_trait_roles_length][1][rolecount][2]

                all_role_ids.append(nfttrait_roleid)

                conn = get_db_connection()
                nft_balance = 0
                try:
                    with conn.cursor() as cur:
                        cur.execute("SELECT COUNT(*) FROM allnfts WHERE \"{}\" = %s AND \"discordid\" = %s AND \"collectionaddress\" = %s".format(nft_trait_type), (nft_trait_value, discord_id, collectionaddress))
                        result = cur.fetchone()
                        nft_balance = result[0] if result else 0
                        print(nft_balance)
                except Exception as e:
                    print(f"Couldn't query the database: {str(e)}")

                if nft_balance > 0:
                    role_ids_to_add.append(nfttrait_roleid)
                    print(f"Added role {nfttrait_roleid} for {get_collection_name(collectionaddress)}")
                else:
                    print(f"No NFTs with trait {nft_trait_value} for {get_collection_name(collectionaddress)}")

                rolecount -= 1


            nft_trait_roles_length -= 1
    except:
        print("Could not process NFT trait rules")


    role_ids_to_add = list(set(role_ids_to_add))

    all_role_ids =  list(set(all_role_ids))

    roles_to_remove = []

    for role in all_role_ids:
        if role not in role_ids_to_add:
            roles_to_remove.append(role)



    print(f"Roles to add: {role_ids_to_add}")
    print(f"Roles to remove: {roles_to_remove}")

    return role_ids_to_add, roles_to_remove



def getShowRoleList(guild_id):
    output = f""""""
    token_roles_list = []
    nft_count_roles_list = []
    nft_trait_roles_list = []

    try:
        # Get the directory of the currently executing script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the relative path to the JSON file
        file_path = os.path.join(script_dir, f"rosy/guild_configs/guild_{guild_id}.json")

        with open(file_path, 'r') as file:
            json_data = json.load(file)
            
    
        token_roles = json_data.get("TOKEN_ROLES", {})
        token_roles_list = list(token_roles.items())


        nft_count_roles = json_data.get("NFT_COUNT_ROLES", {})
        nft_count_roles_list = list(nft_count_roles.items())

        nft_trait_roles = json_data.get("NFT_TRAIT_ROLES", {})
        nft_trait_roles_list = list(nft_trait_roles.items())
    except Exception as e:
        print(f"Cannot add roles for tokens: {e}")


    if len(token_roles_list) > 0:
        output = output + f"""Token rules: \n\n"""
        for tokenlists in token_roles_list:
            #print(tokenlists)
            for tokenrule in tokenlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""Own {tokenrule[0]} of {get_token_name(tokenlists[0])} for {tokenrule[1]} \n"""

    if len(nft_count_roles_list) > 0:
        output = output + f"""\n\nNFT count rules: \n\n"""
        for nftlists in nft_count_roles_list:
            #print(tokenlists)
            for nftrule in nftlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""Own {nftrule[0]} {getNftNameCount(nftrule[0])} of {get_collection_name(nftlists[0])} to get the {nftrule[1]} role \n"""


    if len(nft_trait_roles_list) > 0:
        output = output + f"""\n\nNFT count rules: \n\n"""
        for nftlists in nft_trait_roles_list:
            #print(tokenlists)
            for nftrule in nftlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""Own an NFT of {get_collection_name(nftlists[0])} with the {nftrule[1]} {nftrule[0]} trait to get {nftrule[2]} role \n"""

    return output


role_ids_to_add, roles_to_remove = tokenroles(1226789689323819008, 0)
print(roles_to_remove)