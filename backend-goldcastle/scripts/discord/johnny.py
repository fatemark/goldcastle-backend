import discord
import psycopg2
from discord.ext import commands, tasks
import asyncio
import os
from response import generate_response, generate_compliment_johnny
from audio import elevenlabs
import random
from deleteaudio import delete_audio_files
import json
from small_dependency import get_bot_username, get_bot_avatar, numberresult, get_token_name, get_collection_name, getguilds, getroleschannel, getverificationchannel, get_deletion_exclusion, remove_quotes_if_present, getNftNameCount
from roles_adder import tokenroles
import shutil
from discord import app_commands, ui

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

johnny_channel_id = 1225194470769823784


exception_role_ids = [1225259113651634217, 1226134206183243787]

# Database connection details
db_config = {
    'host': 'postgres',
    'database': 'goldcastle',
    'user': 'esse',
    'password': '96509035'
}

def get_db_connection():
    return psycopg2.connect(**db_config)

class GenderSelectionView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.gender = None

    @discord.ui.button(label='Male', style=discord.ButtonStyle.primary, custom_id='male_button')
    async def male_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.gender = 'Male'
        await interaction.response.send_message(f"{interaction.user.mention}, you selected Male. I will now check your $GOLD and NFT balance")
        self.stop()

    @discord.ui.button(label='Female', style=discord.ButtonStyle.danger, custom_id='female_button')
    async def female_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.gender = 'Female'
        await interaction.response.send_message(f"{interaction.user.mention}, you selected Female. I will now check your $GOLD and NFT balance")
        self.stop()

    @discord.ui.button(label='DUCK', style=discord.ButtonStyle.secondary, custom_id='duck_button')
    async def duck_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.gender = 'Other (DUCK)'
        await interaction.response.send_message(f"{interaction.user.mention}, you selected Other (DUCK). I will now check your $GOLD and NFT balance")
        self.stop()

    @discord.ui.button(label='IDK', style=discord.ButtonStyle.success, custom_id='idk_button')
    async def idk_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.gender = 'Other (IDK)'
        await interaction.response.send_message(f"{interaction.user.mention}, you selected Other (IDK). I will now check your $GOLD and NFT balance")
        self.stop()



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync()
    print('Commands synced.')
    bot.loop.create_task(check_roles())



@bot.tree.command(name='verify', description='Sign to verify NFT and Token ownership')
async def verify(interaction: discord.Interaction):
    verification_channel_id = 1225296606266523648  # Replace with the actual channel ID
    if interaction.channel.id == verification_channel_id or interaction.channel.id == johnny_channel_id:
        discord_id = interaction.user.id
        redirect_url = f'https://goldcastle.club/sign/{discord_id}'
        
        # Create an embed with the preview image
        embed = discord.Embed(title='Verification', description='Click here to verify $GOLD and NFT ownership:', color=0x00ff00)
        embed.set_thumbnail(url='https://xasdsxuik7lxfsh5ugx3at6of2bxjihsbk45linvxgjalpqquxoq.arweave.net/uCQ5XohX13LI_aGvsE_OLoN0oPIKudWhtbmSBb4Qpd0')
        
        # Create a button with the redirect URL
        button = discord.ui.Button(label='Verify', style=discord.ButtonStyle.url, url=redirect_url)
        view = discord.ui.View()
        view.add_item(button)
        
        await interaction.response.send_message(embed=embed, view=view)
        
        # Wait for a few minutes before checking the database
        await asyncio.sleep(30)  # Adjust the delay as needed
        
        gender_view = GenderSelectionView(interaction)
        await interaction.followup.send(f"{interaction.user.mention}, please select your gender:", view=gender_view)
        
        # Wait for the user to select a gender
        await gender_view.wait()
        
        if gender_view.gender is None:
            await interaction.followup.send(f"{interaction.user.mention}, gender selection timed out. Defaulting to 'Male'.")
            gender = 'Male'
        else:
            gender = gender_view.gender
        
        print("gender:", gender)
        await asyncio.sleep(60)


        # Connect to the database
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Check the goldowners table
                cur.execute('SELECT goldbalance FROM goldowners WHERE discordid = %s', (discord_id,))
                result = cur.fetchone()
                gold_balance = result[0] if result else 0
                
                print("Gold Balance:" ,gold_balance)

                highest_nft_row = -1
                try:
                    # Check the nft_goldcastle_asia table
                    cur.execute('SELECT rarity FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY rarity DESC LIMIT 1', (discord_id,))
                    highestrarity = cur.fetchone()
                    highest_nft_row = highestrarity[0]
                except:
                    highest_nft_row = -1

                print("Your highest NFT is rarity: ", highest_nft_row)
                
                # Assign roles based on gold balance and NFT traits
                guild = interaction.guild
                print(discord_id)
                print(guild.id)  # Print the guild ID instead of the guild name
                member = guild.get_member(discord_id)

                for role in member.roles:
                    if role.id not in exception_role_ids:
                        await member.remove_roles(role)



                print(member.id)  # Print the member ID instead of the member name
                if gold_balance > 1000000000:
                    role = discord.utils.get(guild.roles, id=1225247747242721361)  # role_id_lord_of_gold
                    await member.add_roles(role)                
                elif gold_balance > 222222222:
                    role = discord.utils.get(guild.roles, id=1225247288692183200)  # role_id_king_midas
                    await member.add_roles(role)                
                elif gold_balance > 22222222:
                    role = discord.utils.get(guild.roles, id=1225246714160611418)  # role_id_gold_merchant
                    await member.add_roles(role)
                elif gold_balance > 300000:
                    role = discord.utils.get(guild.roles, id=1225246509596151968)  # gold boy
                    await member.add_roles(role)




                if highest_nft_row == 0:
                    role_id = 1225243380880244806 if gender == 'Other (DUCK)' else 1225243027900076103  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 1:
                    role_id = 1225243597415256094 if gender == 'Female' else 1216739636559220888  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 2:
                    role_id = 1225243867079512145 if gender == 'Female' else 1225243738285150279  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 3:
                    role_id = 1225257235928580266 if gender == 'Female' else 1216739587750367323  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 4:
                    role_id = 1225257732861333585 if gender == 'Female' else 1216739542170730567  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 5:
                    role_id = 1225258985565720677 if gender == 'Female' else 1216739311655850134  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 6:
                    role_id = 1225257082375377016 if gender == 'Female' else 1216739436344119428  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 7:
                    role_id = 1225259114888826932 if gender == 'Female' else 1216739208434028565  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)               
                if highest_nft_row == 8:
                    if gender == 'Female':
                        role_id = 1225259114075000904 
                    elif gender == 'Other (DUCK)':
                        role_id = 1225259113651634217
                    else:
                        role_id = 1216739107376599150

                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 9:
                    role_id = 1216739039789580338 
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 10:
                    role_id = 1216738943161204747
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   
                if highest_nft_row == 11:
                    role_id = 1216738742866284595
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 12:
                    role_id = 1216738601644199986
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   
                if highest_nft_row == 13:
                    role_id = 1216738392885432340
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 14:
                    role_id = 1225261021640265870
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   



                vassalcount = 0
                try:
                    # Check the nft_goldcastle_asia table
                    cur.execute('SELECT members FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY members DESC LIMIT 1', (discord_id,))
                    vassals = cur.fetchone()
                    vassalcount = vassals[0]
                    print(f"Vassalcount: {vassalcount}")
                except:
                    vassalcount = 0


                if vassalcount >= 77:
                    role_id = 1225264267897340025
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 55:
                    role_id = 1225263970672185405
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 44:
                    role_id = 1225263751142572102
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 32:
                    role_id = 1225263562738368573
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 22:
                    role_id = 1225263348229210112
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 14:
                    role_id = 1225263194012909678
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 7:
                    role_id = 1225262954744647680
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   







                cur.execute('UPDATE goldbalance SET goldowners = %s WHERE discordid = %s', (gender, discord_id,))


                await interaction.response.send_message("Verification and role assignment completed successfully!")
        except Exception as e:
            print(f"An error occurred during verification: {str(e)}")
            await interaction.response.send_message(f"{interaction.user.mention} Roles have not been processed. Try to call !roles in a few minutes. If that fails try to call verify! again")
        finally:
            conn.close()
    else:
        await interaction.response.send_message("Not allowed here :imp: Try this command in the roles channel :smiling_imp:")


@bot.tree.command(name='roles', description='Johnny Checking roles')
async def roles(interaction: discord.Interaction):
    verification_channel_id = 1225296606266523648  # Replace with the actual channel ID

    if interaction.channel.id == verification_channel_id or interaction.channel.id == johnny_channel_id:
        discord_id = interaction.user.id
        view = GenderSelectionView(interaction)
        await interaction.response.send_message(f"{interaction.user.mention}, please select your gender:", view=view, ephemeral=True)

        # Wait for the user to select a gender
        await view.wait()

        if view.gender is None:
            await interaction.followup.send(f"{interaction.user.mention}, gender selection timed out. Defaulting to 'Male'.")
            gender = 'Male'
        else:
            gender = view.gender
        

        await asyncio.sleep(1)

        # Connect to the database
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                # Check the goldowners table
                cur.execute('SELECT goldbalance FROM goldowners WHERE discordid = %s', (discord_id,))
                result = cur.fetchone()
                gold_balance = result[0] if result else 0
                

                highest_nft_row = -1
                try:
                    # Check the nft_goldcastle_asia table
                    cur.execute('SELECT rarity FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY rarity DESC LIMIT 1', (discord_id,))
                    highestrarity = cur.fetchone()
                    highest_nft_row = highestrarity[0]
                except:
                    highest_nft_row = -1

                print("Your highest NFT is rarity: ", highest_nft_row)
                
                # Assign roles based on gold balance and NFT traits
                guild = interaction.guild
                member = guild.get_member(discord_id)
                for role in member.roles:
                    if role.id not in exception_role_ids:
                        try:
                            await member.remove_roles(role)
                        except:
                            print("Could not remove role")



                if gold_balance > 1000000000:
                    role = discord.utils.get(guild.roles, id=1225247747242721361)  # role_id_lord_of_gold
                    await member.add_roles(role)                
                elif gold_balance > 222222222:
                    role = discord.utils.get(guild.roles, id=1225247288692183200)  # role_id_king_midas
                    await member.add_roles(role)                
                elif gold_balance > 22222222:
                    role = discord.utils.get(guild.roles, id=1225246714160611418)  # role_id_gold_merchant
                    await member.add_roles(role)
                elif gold_balance > 300000:
                    role = discord.utils.get(guild.roles, id=1225246509596151968)  # gold boy
                    await member.add_roles(role)




                if highest_nft_row == 0:
                    role_id = 1225243380880244806 if gender == 'Other (DUCK)' else 1225243027900076103  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 1:
                    role_id = 1225243597415256094 if gender == 'Female' else 1216739636559220888  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 2:
                    role_id = 1225243867079512145 if gender == 'Female' else 1225243738285150279  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 3:
                    role_id = 1225257235928580266 if gender == 'Female' else 1216739587750367323  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 4:
                    role_id = 1225257732861333585 if gender == 'Female' else 1216739542170730567  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 5:
                    role_id = 1225258985565720677 if gender == 'Female' else 1216739311655850134  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 6:
                    role_id = 1225257082375377016 if gender == 'Female' else 1216739436344119428  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 7:
                    role_id = 1225259114888826932 if gender == 'Female' else 1216739208434028565  # Use role IDs
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)               
                if highest_nft_row == 8:
                    if gender == 'Female':
                        role_id = 1225259114075000904 
                    elif gender == 'Other (DUCK)':
                        role_id = 1225259113651634217
                    else:
                        role_id = 1216739107376599150

                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 9:
                    role_id = 1216739039789580338 
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 10:
                    role_id = 1216738943161204747
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   
                if highest_nft_row == 11:
                    role_id = 1216738742866284595
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 12:
                    role_id = 1216738601644199986
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   
                if highest_nft_row == 13:
                    role_id = 1216738392885432340
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                if highest_nft_row == 14:
                    role_id = 1225261021640265870
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   



                vassalcount = 0
                try:
                    # Check the nft_goldcastle_asia table
                    cur.execute('SELECT members FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY members DESC LIMIT 1', (discord_id,))
                    vassals = cur.fetchone()
                    vassalcount = vassals[0]
                    print(f"Vssalcount {vassalcount}")
                except:
                    vassalcount = 0

                if vassalcount >= 77:
                    role_id = 1225264267897340025
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 55:
                    role_id = 1225263970672185405
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 44:
                    role_id = 1225263751142572102
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 32:
                    role_id = 1225263562738368573
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 22:
                    role_id = 1225263348229210112
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 14:
                    role_id = 1225263194012909678
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)
                elif vassalcount >= 7:
                    role_id = 1225262954744647680
                    role = discord.utils.get(guild.roles, id=role_id)
                    await member.add_roles(role)   


                cur.execute('UPDATE goldbalance SET goldowners = %s WHERE discordid = %s', (gender, discord_id,))

                await interaction.followup.send("Verification and role assignment completed successfully!")
        except Exception as e:
            print(f"An error occurred during verification: {str(e)}")
            await interaction.followup.send(f"{interaction.user.mention} Roles have not been processed. Try to call !roles in a few minutes. If that fails try to call verify! again")
        finally:
            conn.close()

    else:
        await interaction.followup.send("Not allowed here :imp: Try this command in the roles channel :smiling_imp:")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        highest_role_id = message.author.top_role.id
        username = message.author.name

        user_message = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        
        # Check if the bot mention is still present in the user message
        if f'<@{bot.user.id}>' in user_message:
            user_message = user_message.replace(f'<@{bot.user.id}>', '').strip()
        
        print(highest_role_id, username, user_message)
        response = generate_response(user_message, highest_role_id, username)


        audiochance = random.randint(0, 200)
        if audiochance == 77:
            delete_audio_files()
            voice_id = "Hjzqw9NR0xFMYU9Us0DL"
            audio_file = elevenlabs(response, voice_id)
            if audio_file:
                with open(audio_file, "rb") as f:
                    voice_message = discord.File(f)
                    await message.channel.send(file=voice_message)
            else:
                await message.channel.send("Failed to generate voice message.")
        else:
            await message.channel.send(response)


    await bot.process_commands(message)


@bot.tree.command(name='showroles', description='Show all available roles')
async def showroles(interaction: discord.Interaction):
    roles_message = f"""
These are all roles and requirements:

Phoenix: Own a Rarity :one::four: NFT

Eternal: Own a Rarity :one::three: NFT

Galactic Empire: Have 77 vassals :stars:

Universal: Own a Rarity :one::two: NFT
 
Planetary Dominion: Have 55 vassals :ringed_planet:

Dominator: Own a Rarity :one::one: NFT

god: Own a Rarity :one::zero: NFT 

Planetator: Own a Rarity :nine: NFT

LORD OF $GOLD: Be a $GOLD billionaire :whale:

Dragon: Own a dragon type NFT

Heavenly Kingdom: Have 44 vassals :wing:

Emperor/Empress: Own a Rarity :eight: NFT or be a superior Duck

High Kingdom: Have 32 vassals :crown:

King/Queen: Own a Rarity :seven: NFT

King Midas: Have 222,222,222 $GOLD :money_with_wings:

Grand Duke/Duchess: Own a Rarity :six: NFT

Principality: Have 22 vassals :crossed_swords:

Prince/Princess: Own a Rarity :five: NFT

Small Duchy: Have 14 vassals :european_castle:

Duke/Duchess: Own a Rarity :four: NFT

$GOLD Merchant: Have 22,222,222 $GOLD :moneybag:

Baron/Baroness: Own a Rarity :three: NFT

Lord/Lady: Own a Rarity :two: NFT

Peasant Hoarder: Have 7 vassals :farmer:

Knight/Swordmaiden: Own a Rarity :one: NFT

Peasant/McDuck: Own a Rarity :zero: NFT
"""
    
    await interaction.response.send_message(roles_message)


@bot.tree.command(name='johnnycommands', description='Show all available commands')
async def johnnycommands(interaction: discord.Interaction):
    roles_message = f"""
/verify = Sign and tell Johnny what your wallet is
/roles = Let Johnny check your roles
/showroles = Show all available roles and requirements
/showcommands = Show all available commands
/compliment = Let Johnny compliment a random member
/complimentrelay = Let Johnny give a compliment to a specific member
"""
    await interaction.response.send_message(roles_message)   

@bot.event
async def on_member_join(member):
    # Get the welcome channel
    welcome_channel = member.guild.get_channel(1226131651256651818)
    if welcome_channel:
        # Assign the 'new' role to new members
        new_role = member.guild.get_role(1226131919595372564)
        if new_role:
            await member.add_roles(new_role)

@bot.event
async def on_raw_reaction_add(payload):
    # Check if the reaction is added in the specific channel
    if payload.channel_id == 1226131651256651818:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        # Assign the 'verified' role to the member
        role = guild.get_role(1226134206183243787)
        if role:
            await member.add_roles(role)


@bot.tree.command(name='compliment', description='Let Johnny compliment a random member')
async def compliment(interaction: discord.Interaction):
    member = random.choice(interaction.guild.members)
    username = member.display_name
    complimentintiator = interaction.user.display_name
    
    # Get the top role ID of the member
    top_role_id = member.top_role.id
    
    # Get the username of the member
    username = member.display_name
    subject = ""
    compliment = generate_compliment_johnny(top_role_id, username, complimentintiator, subject)
    
    audiochance = random.randint(0, 200)
    if audiochance == 77:
        delete_audio_files()
        voice_id = "Hjzqw9NR0xFMYU9Us0DL"
        audio_file = elevenlabs(compliment, voice_id)
        if audio_file:
            with open(audio_file, "rb") as f:
                voice_message = discord.File(f)
            await interaction.channel.send(f"{member.mention}\n{compliment}", file=voice_message)
        else:
            await interaction.channel.send("Failed to generate voice message.")
    else:
        await interaction.channel.send(f"{member.mention}\n{compliment}")



@bot.tree.command(name='complimentrelay', description='Let Johnny compliment a member on a specific subject')
async def complimentrelay(interaction: discord.Interaction, member: discord.Member, subject: str):
    complimentUserName = interaction.user.display_name
    username = member.display_name
    top_role_id = member.top_role.id
    response = generate_compliment_johnny(top_role_id, username, complimentUserName, subject)
    response = remove_quotes_if_present(response)
    
    audiochance = random.randint(0, 200)
    if audiochance == 77:
        delete_audio_files()
        voice_id = "Hjzqw9NR0xFMYU9Us0DL"
        audio_file = elevenlabs(response, voice_id)
        if audio_file:
            with open(audio_file, "rb") as f:
                voice_message = discord.File(f)
            await interaction.channel.send(f"{member.mention}\n{response}", file=voice_message)
        else:
            await interaction.channel.send("Failed to generate voice message.")
    else:
        await interaction.channel.send(f"{member.mention}\n{response}")




async def check_roles():
    while True:
        process = await asyncio.create_subprocess_exec(
            'node', 'check_gold_balance.mjs',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the subprocess to complete
        stdout, stderr = await process.communicate()

        # Check the subprocess exit code
        if process.returncode == 0:
            print("MJS script executed successfully")
            print(f"Output: {stdout.decode()}")
        else:
            print("MJS script execution failed")
            print(f"Error: {stderr.decode()}")


        guild = bot.get_guild(1209978326089728020)  # Replace with your actual guild ID
        for member in guild.members:
            discord_id = member.id


            conn = get_db_connection()
            try:
                with conn.cursor() as cur:
                    # Check the goldowners table
                    cur.execute('SELECT goldbalance, gender FROM goldowners WHERE discordid = %s', (discord_id,))
                    result = cur.fetchone()

                    if result:
                        gold_balance, gender = result
                    else:
                        gold_balance, gender = 0, "Male"

                    highest_nft_row = -1
                    
                    try:
                        # Check the nft_goldcastle_asia table
                        cur.execute('SELECT rarity FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY rarity DESC LIMIT 1', (discord_id,))
                        highestrarity = cur.fetchone()
                        highest_nft_row = highestrarity[0] if highestrarity else -1
                    except:
                        highest_nft_row = -1

                    print(f"Member: {member.name} - Highest NFT Rarity: {highest_nft_row}")

                    
                    member = guild.get_member(discord_id)

                    for role in member.roles:
                        if role.id not in exception_role_ids:
                            try:
                                await member.remove_roles(role)
                            except:
                                print("Could not remove")

                    print(f"Moving onto finding roles for {member.name}")
                    if gold_balance > 1000000000:
                        role = discord.utils.get(guild.roles, id=1225247747242721361)  # role_id_lord_of_gold
                        await member.add_roles(role)                
                    elif gold_balance > 222222222:
                        role = discord.utils.get(guild.roles, id=1225247288692183200)  # role_id_king_midas
                        await member.add_roles(role)                
                    elif gold_balance > 22222222:
                        role = discord.utils.get(guild.roles, id=1225246714160611418)  # role_id_gold_merchant
                        await member.add_roles(role)
                    elif gold_balance > 300000:
                        role = discord.utils.get(guild.roles, id=1225246509596151968)  # gold boy
                        await member.add_roles(role)


                    if highest_nft_row == 0:
                        role_id = 1225243380880244806 if gender == 'Other (DUCK)' else 1225243027900076103  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 1:
                        role_id = 1225243597415256094 if gender == 'Female' else 1216739636559220888  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 2:
                        role_id = 1225243867079512145 if gender == 'Female' else 1225243738285150279  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 3:
                        role_id = 1225257235928580266 if gender == 'Female' else 1216739587750367323  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 4:
                        role_id = 1225257732861333585 if gender == 'Female' else 1216739542170730567  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 5:
                        role_id = 1225258985565720677 if gender == 'Female' else 1216739311655850134  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 6:
                        role_id = 1225257082375377016 if gender == 'Female' else 1216739436344119428  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 7:
                        role_id = 1225259114888826932 if gender == 'Female' else 1216739208434028565  # Use role IDs
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)               
                    if highest_nft_row == 8:
                        if gender == 'Female':
                            role_id = 1225259114075000904 
                        elif gender == 'Other (DUCK)':
                            role_id = 1225259113651634217
                        else:
                            role_id = 1216739107376599150

                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 9:
                        role_id = 1216739039789580338 
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 10:
                        role_id = 1216738943161204747
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)   
                    if highest_nft_row == 11:
                        role_id = 1216738742866284595
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 12:
                        role_id = 1216738601644199986
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)   
                    if highest_nft_row == 13:
                        role_id = 1216738392885432340
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    if highest_nft_row == 14:
                        role_id = 1225261021640265870
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)   



                    vassalcount = 0
                    try:
                        # Check the nft_goldcastle_asia table
                        cur.execute('SELECT members FROM nft_goldcastle_asia WHERE discordid = %s ORDER BY members DESC LIMIT 1', (discord_id,))
                        vassals = cur.fetchone()
                        vassalcount = vassals[0]
                        print(f"Vassalcount: {vassalcount}")
                    except:
                        vassalcount = 0

                    if vassalcount >= 77:
                        role_id = 1225264267897340025
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 55:
                        role_id = 1225263970672185405
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 44:
                        role_id = 1225263751142572102
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 32:
                        role_id = 1225263562738368573
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 22:
                        role_id = 1225263348229210112
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 14:
                        role_id = 1225263194012909678
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)
                    elif vassalcount >= 7:
                        role_id = 1225262954744647680
                        role = discord.utils.get(guild.roles, id=role_id)
                        await member.add_roles(role)   

            except Exception as e:
                print(f"An error occurred during checking: {str(e)}")
            finally:
                conn.close()
        await asyncio.sleep(3600)  # Wait for 1 hour (3600 seconds)



bot_token = os.environ.get('JOHNNY_DISCORD_BOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Bot token not found in the environment variables.")