import discord
import psycopg2
from discord.ext import commands, tasks
import asyncio
import os
from rosy_response import generate_response
from audio import elevenlabs
import random
from deleteaudio import delete_audio_files
import json
from small_dependency import get_bot_username, get_bot_avatar, numberresult, get_token_name, get_collection_name, getguilds, getroleschannel, getverificationchannel, get_deletion_exclusion
from roles_adder import tokenroles
import shutil

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', self_bot=False, intents=intents)

# Database connection details
db_config = {
    'host': 'postgres',
    'database': 'goldcastle',
    'user': 'esse',
    'password': '96509035'
}

def get_db_connection():
    return psycopg2.connect(**db_config)

@bot.command(name='rosyverify', description='Verify your account')
async def verify(ctx):
    guild_id = ctx.guild.id

    verification_channel_id = getverificationchannel(guild_id)


    if ctx.channel.id == verification_channel_id or verification_channel_id == "":
        discord_id = ctx.author.id

        redirect_url = f'http://localhost:3000/rosy/sign/{discord_id}'
        
        # Create an embed with the preview image
        embed = discord.Embed(title='Verification', description='Click here to verify your token and NFT ownership:', color=0x00ff00)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1227390179921104936/1227390229045055498/rosy.png?ex=66283b3a&is=6615c63a&hm=8bf664e34671662147102a90e6a728c3144cb82d2f7dfa70664ec66a1930b6d8&')
        
        # Create a button with the redirect URL
        button = discord.ui.Button(label='Verify', style=discord.ButtonStyle.url, url=redirect_url)
        view = discord.ui.View()
        view.add_item(button)
        
        await ctx.send(embed=embed, view=view)


@bot.command(name='rosyconfigure', description='Configure guild settings')
@commands.has_permissions(administrator=True)
async def configure(ctx):

    guild_id = ctx.guild.id
    guild_config_path = f"rosy/guild_configs/guild_{guild_id}.json"
    template_path = "rosy/guild_configs/template.json"
    
    if not os.path.exists(guild_config_path):
        # If the guild config file doesn't exist, copy the template file
        shutil.copy(template_path, guild_config_path)
        await ctx.send(f":new: Configuration created :new:")

    



    # Create buttons for selecting the configuration type
    token_roles_button = discord.ui.Button(label='TOKEN_ROLES', style=discord.ButtonStyle.blurple)
    nft_trait_roles_button = discord.ui.Button(label='NFT_TRAIT_ROLES', style=discord.ButtonStyle.green)
    nft_count_roles_button = discord.ui.Button(label='NFT_COUNT_ROLES', style=discord.ButtonStyle.red)

    async def token_roles_callback(interaction):
        # Handle TOKEN_ROLES configuration
        await interaction.response.send_message("Please enter the token ID:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            token_id_message = await bot.wait_for('message', check=check, timeout=120)
            token_id = token_id_message.content.strip()
            tokensymbol = get_token_name(token_id)

            token_roles = []
            i = 1
            while True:
                await ctx.send(f"""
{numberresult(i)} :moneybag: | New {tokensymbol} rule
Enter the AMOUNT of {tokensymbol} needed for this role (or message 'done' to finish :cat2:):
""")
                amount_message = await bot.wait_for('message', check=check, timeout=120)
                if amount_message.content.strip().lower() == 'done':
                    break
                amount = amount_message.content.strip()

                # Create a dropdown with available roles
                role_options = [discord.SelectOption(label=role.name, value=role.id) for role in ctx.guild.roles]
                role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                async def role_dropdown_callback(interaction):
                    selected_role = interaction.guild.get_role(int(interaction.data['values'][0]))
                    token_roles.append((int(amount), selected_role.id))
                    await interaction.response.send_message(f"Created new {tokensymbol} rule for role: {selected_role.name}")

                role_dropdown.callback = role_dropdown_callback
                
                role_dropdown_view = discord.ui.View()
                role_dropdown_view.add_item(role_dropdown)
                await ctx.send(f"New token rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                # Wait for the role selection
                await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                i += 1

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['TOKEN_ROLES']:
                config['TOKEN_ROLES'][token_id] = []
            config['TOKEN_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)

            await ctx.send("Updated successfully!")

        except asyncio.TimeoutError:
            await ctx.send("Configuration timed out. Please try again.")

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['TOKEN_ROLES']:
                config['TOKEN_ROLES'][token_id] = []
            config['TOKEN_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)



    async def nft_trait_roles_callback(interaction):
        # Handle TOKEN_ROLES configuration
        await interaction.response.send_message("Please enter the NFT address:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            token_id_message = await bot.wait_for('message', check=check, timeout=120)
            token_id = token_id_message.content.strip()

            collection_name = get_collection_name(token_id)

            token_roles = []
            i = 1
            while True:
                await ctx.send(f"""
{numberresult(i)} :art: | New nft trait rule for {collection_name}
Enter the TRAIT TYPE to configure (or message 'done' to finish :cat2:):
""")
                amount_message = await bot.wait_for('message', check=check, timeout=120)
                if amount_message.content.strip().lower() == 'done':
                    break
                trait_type = amount_message.content.strip()

                await ctx.send(f"""
{numberresult(i)} :art:
Enter the TRAIT VALUE to configure (or message 'done' to finish :cat2:):
""")
                value__message = await bot.wait_for('message', check=check, timeout=120)
                if value__message.content.strip().lower() == 'done':
                    break
                trait_value = value__message.content.strip()


                # Create a dropdown with available roles
                role_options = [discord.SelectOption(label=role.name, value=role.id) for role in ctx.guild.roles]
                role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                async def role_dropdown_callback(interaction):
                    selected_role = interaction.guild.get_role(int(interaction.data['values'][0]))
                    token_roles.append((trait_type, trait_value, selected_role.id))
                    await interaction.response.send_message(f"Created new {collection_name} trait rule {numberresult(i)} for role: {selected_role.name}")

                role_dropdown.callback = role_dropdown_callback
                role_dropdown_view = discord.ui.View()
                role_dropdown_view.add_item(role_dropdown)
                await ctx.send(f"New nft trait rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                # Wait for the role selection
                await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                i += 1

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['NFT_TRAIT_ROLES']:
                config['NFT_TRAIT_ROLES'][token_id] = []
            config['NFT_TRAIT_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)

            await ctx.send("Updated successfully!")

        except asyncio.TimeoutError:
            await ctx.send("Configuration timed out. Please try again.")

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['NFT_TRAIT_ROLES']:
                config['NFT_TRAIT_ROLES'][token_id] = []
            config['NFT_TRAIT_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)


    async def nft_count_roles_callback(interaction):
        # Handle TOKEN_ROLES configuration
        await interaction.response.send_message("Please enter the contract address:")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            token_id_message = await bot.wait_for('message', check=check, timeout=120)
            token_id = token_id_message.content.strip()

            collection_name = get_collection_name(token_id)
            
            token_roles = []
            i = 1
            while True:
                await ctx.send(f"""
{numberresult(i)} :chart_with_upwards_trend: | New NFT count rule for {collection_name}
Enter the AMOUNT of NFTs needed for this role (or message 'done' to finish :cat2:):
""")
                amount_message = await bot.wait_for('message', check=check, timeout=120)
                if amount_message.content.strip().lower() == 'done':
                    break
                amount = amount_message.content.strip()

                # Create a dropdown with available roles
                role_options = [discord.SelectOption(label=role.name, value=role.id) for role in ctx.guild.roles]
                role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                async def role_dropdown_callback(interaction):
                    selected_role = interaction.guild.get_role(int(interaction.data['values'][0]))
                    token_roles.append((int(amount), selected_role.id))
                    await interaction.response.send_message(f"Created a  new {collection_name} NFT count rule {numberresult(i)} for role: {selected_role.name}")

                role_dropdown.callback = role_dropdown_callback
                role_dropdown_view = discord.ui.View()
                role_dropdown_view.add_item(role_dropdown)
                await ctx.send(f"New NFT count rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                # Wait for the role selection
                await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                i += 1

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['NFT_COUNT_ROLES']:
                config['NFT_COUNT_ROLES'][token_id] = []
            config['NFT_COUNT_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)

            await ctx.send("Updated successfully!")

        except asyncio.TimeoutError:
            await ctx.send("Configuration timed out. Please try again.")

            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
                config = json.load(f)
            if token_id not in config['NFT_COUNT_ROLES']:
                config['NFT_COUNT_ROLES'][token_id] = []
            config['NFT_COUNT_ROLES'][token_id].append(token_roles)
            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                json.dump(config, f, indent=4)


    token_roles_button.callback = token_roles_callback
    nft_trait_roles_button.callback = nft_trait_roles_callback
    nft_count_roles_button.callback = nft_count_roles_callback

    view = discord.ui.View()
    view.add_item(token_roles_button)
    view.add_item(nft_trait_roles_button)
    view.add_item(nft_count_roles_button)

    await ctx.send("Please select the configuration type:", view=view)


@bot.command(name='rosyconfiguration', description='View and manage existing rules')
@commands.has_permissions(administrator=True)
async def configuration(ctx):
    # Create buttons for selecting the configuration type
    token_roles_button = discord.ui.Button(label='TOKEN COUNT ROLES', style=discord.ButtonStyle.blurple)
    
    nft_trait_roles_button = discord.ui.Button(label='NFT TRAIT ROLES', style=discord.ButtonStyle.green)  

    nft_count_roles_button = discord.ui.Button(label='NFT COUNT ROLES', style=discord.ButtonStyle.red)  



    async def token_roles_callback(interaction):
        with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)
        token_roles = config['TOKEN_ROLES']

        if not token_roles:
            await interaction.response.send_message("No TOKEN_ROLES rules found.")
            return

        token_options = []
        for token_id in token_roles.keys():
            token_options.append(discord.SelectOption(label=f"Token: {get_token_name(token_id)}", value=token_id))

        async def token_selected(select_interaction):
            selected_token_id = select_interaction.data['values'][0]
            selected_roles = token_roles[selected_token_id][0]  # Access the first element of the nested array

            if not selected_roles:
                await select_interaction.response.send_message(f"No roles found for Token ID: {selected_token_id}")
                return

            rule_options = []
            for i, role_data in enumerate(selected_roles, start=1):
                amount, role_id = role_data
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_roles[rule_index]

                role_text = f"Token ID: {selected_token_id}\n"
                amount, role_id = selected_rule
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                role_text += f"Amount: {amount}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)


                async def edit_button_callback(button_interaction):
                    # Implement edit functionality here
                    await button_interaction.response.send_message("Please enter the new amount for this rule:")

                    def check(m):
                        return m.author == button_interaction.user and m.channel == button_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_amount = int(msg.content.strip())

                        # Create a dropdown for selecting the role
                        role_options = []
                        for role in ctx.guild.roles:
                            role_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                        async def role_dropdown_callback(dropdown_interaction):
                            selected_role_id = int(dropdown_interaction.data['values'][0])

                            # Update the role data in the configuration
                            for i, role_data in enumerate(selected_roles):
                                if role_data[1] == role_id:
                                    selected_roles[i] = [new_amount, selected_role_id]
                                    break

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a token role rule:", view=view)


                        role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)
                        role_dropdown.callback = role_dropdown_callback

                        role_view = discord.ui.View()
                        role_view.add_item(role_dropdown)

                        await button_interaction.followup.send("Please select a role:", view=role_view)

                    except (asyncio.TimeoutError, ValueError):
                        await button_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(button_interaction):
                    # Remove the selected rule from the configuration
                    del selected_roles[rule_index]

                    # If there are no more rules for the token ID, remove the token ID entry
                    if not selected_roles:
                        del token_roles[selected_token_id]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await button_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the token ID, go back to the token selection
                    if not selected_roles:
                        view = discord.ui.View()
                        view.add_item(token_dropdown)
                        await interaction.followup.send("Please select a token ID:", view=view)
                    else:
                        view = discord.ui.View()
                        view.add_item(rule_dropdown)
                        await interaction.followup.send("Please select a rule:", view=view)


                edit_button.callback = edit_button_callback
                delete_button.callback = delete_button_callback

                view = discord.ui.View()
                view.add_item(edit_button)
                view.add_item(delete_button)

                await rule_interaction.response.send_message(role_text, view=view)

            rule_dropdown = discord.ui.Select(placeholder="Select a rule", options=rule_options)
            rule_dropdown.callback = rule_selected

            rule_view = discord.ui.View()
            rule_view.add_item(rule_dropdown)

            await select_interaction.response.send_message("Please select a rule:", view=rule_view)

        token_dropdown = discord.ui.Select(placeholder="Select a token ID", options=token_options)
        token_dropdown.callback = token_selected

        token_view = discord.ui.View()
        token_view.add_item(token_dropdown)

        await interaction.response.send_message("Please select a token ID:", view=token_view)




    async def nft_count_roles_callback(interaction):
        with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)
        token_roles = config['NFT_COUNT_ROLES']

        if not token_roles:
            await interaction.response.send_message("No NFT_COUNT_ROLES rules found.")
            return

        token_options = []
        for token_id in token_roles.keys():
            collection_name = get_collection_name(token_id)
            if collection_name:
                label = collection_name[:100]  # Truncate the label to a maximum of 100 characters
                token_options.append(discord.SelectOption(label=label, value=token_id))

        async def token_selected(select_interaction):
            selected_token_id = select_interaction.data['values'][0]
            selected_roles = token_roles[selected_token_id][0]  # Access the first element of the nested array

            if not selected_roles:
                await select_interaction.response.send_message(f"No NFT count role rules found for {get_collection_name(selected_token_id)}")
                return

            rule_options = []
            for i, role_data in enumerate(selected_roles, start=1):
                amount, role_id = role_data
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_roles[rule_index]

                role_text = f"{get_collection_name(selected_token_id)}\n"
                amount, role_id = selected_rule
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                role_text += f"Amount: {amount}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)


                async def edit_button_callback(button_interaction):
                    # Implement edit functionality here
                    await button_interaction.response.send_message("Please enter the new amount for this rule:")

                    def check(m):
                        return m.author == button_interaction.user and m.channel == button_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_amount = int(msg.content.strip())

                        # Create a dropdown for selecting the role
                        role_options = []
                        for role in ctx.guild.roles:
                            role_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                        async def role_dropdown_callback(dropdown_interaction):
                            selected_role_id = int(dropdown_interaction.data['values'][0])

                            # Update the role data in the configuration
                            for i, role_data in enumerate(selected_roles):
                                if role_data[1] == role_id:
                                    selected_roles[i] = [new_amount, selected_role_id]
                                    break

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a NFT count role rule:", view=view)


                        role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)
                        role_dropdown.callback = role_dropdown_callback

                        role_view = discord.ui.View()
                        role_view.add_item(role_dropdown)

                        await button_interaction.followup.send("Please select a role:", view=role_view)

                    except (asyncio.TimeoutError, ValueError):
                        await button_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(button_interaction):
                    # Remove the selected rule from the configuration
                    del selected_roles[rule_index]

                    # If there are no more rules for the token ID, remove the token ID entry
                    if not selected_roles:
                        del token_roles[selected_token_id]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await button_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the token ID, go back to the token selection
                    if not selected_roles:
                        view = discord.ui.View()
                        view.add_item(token_dropdown)
                        await interaction.followup.send("Please select a collection:", view=view)
                    else:
                        view = discord.ui.View()
                        view.add_item(rule_dropdown)
                        await interaction.followup.send("Please select a rule:", view=view)


                edit_button.callback = edit_button_callback
                delete_button.callback = delete_button_callback

                view = discord.ui.View()
                view.add_item(edit_button)
                view.add_item(delete_button)

                await rule_interaction.response.send_message(role_text, view=view)

            rule_dropdown = discord.ui.Select(placeholder="Select a rule", options=rule_options)
            rule_dropdown.callback = rule_selected

            rule_view = discord.ui.View()
            rule_view.add_item(rule_dropdown)

            await select_interaction.response.send_message("Please select a rule:", view=rule_view)

        token_dropdown = discord.ui.Select(placeholder="Select a collection", options=token_options)
        token_dropdown.callback = token_selected

        token_view = discord.ui.View()
        token_view.add_item(token_dropdown)

        await interaction.response.send_message("Please select a collection:", view=token_view)



    async def nft_trait_roles_callback(interaction):
        with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'r') as f:
            config = json.load(f)
        trait_roles = config['NFT_TRAIT_ROLES']

        if not trait_roles:
            await interaction.response.send_message("No NFT_TRAIT_ROLES rules found.")
            return
        
        collection_options = []
        for collection_address in trait_roles.keys():
            collection_name = get_collection_name(collection_address)
            label = collection_name[:100]
            collection_options.append(discord.SelectOption(label, value=collection_address))

        async def collection_selected(select_interaction):
            selected_collection_address = select_interaction.data['values'][0]
            selected_rules = trait_roles[selected_collection_address][0]  # Access the first element of the nested array

            if not selected_rules:
                await select_interaction.response.send_message(f"No trait role rules for {get_collection_name(selected_collection_address)}")
                return

            rule_options = []
            for i, rule_data in enumerate(selected_rules, start=1):
                trait_type, trait_value, role_id = rule_data
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Trait Type: {trait_type}, Trait Value: {trait_value}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_rules[rule_index]

                role_text = f"{get_collection_name(selected_collection_address)}\n"
                trait_type, trait_value, role_id = selected_rule
                role = discord.utils.get(ctx.guild.roles, id=role_id)
                role_text += f"Trait Type: {trait_type}, Trait Value: {trait_value}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)

                async def edit_button_callback(button_interaction):
                    # Implement edit functionality here
                    await button_interaction.response.send_message("Please enter the new trait type for this rule:")

                    def check(m):
                        return m.author == button_interaction.user and m.channel == button_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_trait_type = msg.content.strip()

                        await button_interaction.followup.send("Please enter the new trait value for this rule:")
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_trait_value = msg.content.strip()

                        # Create a dropdown for selecting the role
                        role_options = []
                        for role in ctx.guild.roles:
                            role_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                        async def role_dropdown_callback(dropdown_interaction):
                            selected_role_id = int(dropdown_interaction.data['values'][0])

                            # Update the role data in the configuration
                            for i, rule_data in enumerate(selected_rules):
                                if rule_data[2] == role_id:
                                    selected_rules[i] = [new_trait_type, new_trait_value, selected_role_id]
                                    break

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a trait role rule:", view=view)

                        role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)
                        role_dropdown.callback = role_dropdown_callback

                        role_view = discord.ui.View()
                        role_view.add_item(role_dropdown)

                        await button_interaction.followup.send("Please select a role:", view=role_view)

                    except (asyncio.TimeoutError, ValueError):
                        await button_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(button_interaction):
                    # Remove the selected rule from the configuration
                    del selected_rules[rule_index]

                    # If there are no more rules for the collection address, remove the collection address entry
                    if not selected_rules:
                        del trait_roles[selected_collection_address]
                    else:
                        trait_roles[selected_collection_address] = [selected_rules]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{ctx.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await button_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the collection address, go back to the collection selection
                    if not selected_rules:
                        view = discord.ui.View()
                        view.add_item(collection_dropdown)
                        await interaction.followup.send("Please select a collection:", view=view)
                    else:
                        view = discord.ui.View()
                        view.add_item(rule_dropdown)
                        await interaction.followup.send("Please select a trait role rule:", view=view)

                edit_button.callback = edit_button_callback
                delete_button.callback = delete_button_callback

                view = discord.ui.View()
                view.add_item(edit_button)
                view.add_item(delete_button)

                await rule_interaction.response.send_message(role_text, view=view)

            rule_dropdown = discord.ui.Select(placeholder="Select a rule", options=rule_options)
            rule_dropdown.callback = rule_selected

            rule_view = discord.ui.View()
            rule_view.add_item(rule_dropdown)

            await select_interaction.response.send_message("Please select a rule:", view=rule_view)

        collection_dropdown = discord.ui.Select(placeholder="Select a collection", options=collection_options)
        collection_dropdown.callback = collection_selected

        collection_view = discord.ui.View()
        collection_view.add_item(collection_dropdown)

        await interaction.response.send_message("Please select a collection:", view=collection_view)


    
    token_roles_button.callback = token_roles_callback
    
    nft_trait_roles_button.callback = nft_trait_roles_callback

    nft_count_roles_button.callback = nft_count_roles_callback


    view = discord.ui.View()
    view.add_item(token_roles_button)

    view.add_item(nft_trait_roles_button)
    
    view.add_item(nft_count_roles_button)


    await ctx.send("Please select the rule type to view:", view=view)





@bot.command(name='rosyroles', description='Checking roles')
async def verify(ctx):
    guildid = ctx.guild.id
    verification_channel_id = getroleschannel(guildid)
    
    if ctx.channel.id == verification_channel_id or verification_channel_id == "":
        member = ctx.author

        discord_id = member.id
        print(discord_id)
        role_ids_to_add, all_role_ids = tokenroles(guildid, discord_id)
        current_roles = member.roles
        print(role_ids_to_add)

        # Get the list of valid role objects in the guild
        guild_roles = ctx.guild.roles

        # Filter out roles that are not in the guild's roles
        valid_roles_to_add = [ctx.guild.get_role(role_id) for role_id in role_ids_to_add if ctx.guild.get_role(role_id) in guild_roles]
        valid_all_roles = [ctx.guild.get_role(role_id) for role_id in all_role_ids if ctx.guild.get_role(role_id) in guild_roles]


        delete_expired, exclusions = get_deletion_exclusion(guildid)

            # Remove roles that are in valid_all_roles but not in valid_roles_to_add and are present in the member's roles
        roles_to_remove = [role for role in current_roles if role in valid_all_roles and role not in valid_roles_to_add]

        if delete_expired:
            # Filter out roles that are in the exclusions array
            roles_to_remove = [role for role in roles_to_remove if role.id not in exclusions]

            for role in roles_to_remove:
                try:
                    await member.remove_roles(role)
                except discord.NotFound:
                    print(f"Role {role.name} not found in the guild. Skipping removal.")
        else:
            print("Role removal is disabled. Skipping role removal.")


        for role_id in role_ids_to_add:
            role = ctx.guild.get_role(role_id)
            if role is not None:
                await member.add_roles(role)


    else:
        await ctx.send("Not allowed here :japanese_ogre:")



@tasks.loop(hours=1)
async def check_roles():
    for guild in bot.guilds:
        for member in guild.members:
            discord_id = member.id
            print(discord_id)
            role_ids_to_add, all_role_ids = tokenroles(guild.id, discord_id)
            current_roles = member.roles
            print(role_ids_to_add)

            # Get the list of valid role objects in the guild
            guild_roles = guild.roles

            # Filter out roles that are not in the guild's roles
            valid_roles_to_add = [guild.get_role(role_id) for role_id in role_ids_to_add if guild.get_role(role_id) in guild_roles]
            valid_all_roles = [guild.get_role(role_id) for role_id in all_role_ids if guild.get_role(role_id) in guild_roles]

            delete_expired, exclusions = get_deletion_exclusion(guild.id)

            # Remove roles that are in valid_all_roles but not in valid_roles_to_add and are present in the member's roles
            roles_to_remove = [role for role in current_roles if role in valid_all_roles and role not in valid_roles_to_add]

            if delete_expired:
                # Filter out roles that are in the exclusions array
                roles_to_remove = [role for role in roles_to_remove if role.id not in exclusions]

                for role in roles_to_remove:
                    try:
                        await member.remove_roles(role)
                    except discord.NotFound:
                        print(f"Role {role.name} not found in the guild. Skipping removal.")
            else:
                print("Role removal is disabled. Skipping role removal.")

            for role_id in role_ids_to_add:
                role = guild.get_role(role_id)
                if role is not None:
                    await member.add_roles(role)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    check_roles.start()



@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        highest_role_name = message.author.top_role.name
        username = message.author.name
        guild = message.guild.name
        user_message = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        
        # Check if the bot mention is still present in the user message
        if f'<@{bot.user.id}>' in user_message:
            user_message = user_message.replace(f'<@{bot.user.id}>', '').strip()
        
        print(highest_role_name, username, user_message)
        response = generate_response(user_message, highest_role_name, username, guild)

        audiochance = random.randint(0, 200)
        if audiochance == 77:
            delete_audio_files()
            voice_id = "vJaMhFRlaZVOFFq8yDs8"
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






def load_config():
    try:
        with open('rosy/guild_configs/guilds_rosy.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"configuration": []}

def save_config(config):
    with open('rosy/guild_configs/guilds_rosy.json', 'w') as file:
        json.dump(config, file, indent=4)


@bot.command(name='rosysettings')
@commands.has_permissions(administrator=True)
async def rosysettings(ctx):
    config = load_config()
    guild_id = ctx.guild.id
    guild_name = ctx.guild.name

    # Check if an entry already exists for the guild
    guild_config = next((c for c in config['configuration'] if c['guild_id'] == guild_id), None)

    if guild_config is None:
        # Create a new entry with default values
        guild_config = {
            "guild_id": guild_id,
            "name": guild_name,
            "usage": 0,
            "tips": 0,
            "personality": "",
            "roleschannel": "",
            "verificationchannel": "",
            "delete_expired": False,
            "exclude_from_deletion": [],
            "botname": ""
        }
        config['configuration'].append(guild_config)
    else:
        # Update the guild name
        guild_config['name'] = guild_name

    # Ask questions to fill in the configuration
    await ctx.send("""
Please answer the following questions to configure the settings:
                   
:exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation: 
Respond with '_' to leave a field unchanged
or use '=' to reset a field to its default value.
:exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation::exclamation: 
\n
                   
""")

    async def ask_question(prompt, current_value, default_value):
        await ctx.send(f"{prompt} (Current: {current_value})")
        response = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        return response.content

    personality = await ask_question(":rage: :grinning: Enter the personality for this guild:", guild_config['personality'], "")
    if personality == '=':
        guild_config['personality'] = ""
    elif personality != '_':
        guild_config['personality'] = personality

    roleschannel_id = await ask_question(":rocket: Enter the ID of the roles channel:", guild_config['roleschannel'], None)
    if roleschannel_id == '=':
        guild_config['roleschannel'] = ""
    elif roleschannel_id != '_':
        guild_config['roleschannel'] = int(roleschannel_id)

    verificationchannel_id = await ask_question(":rotating_light: Enter the ID of the verification channel:", guild_config['verificationchannel'], None)
    if verificationchannel_id == '=':
        guild_config['verificationchannel'] = ""
    elif verificationchannel_id != '_':
        guild_config['verificationchannel'] = int(verificationchannel_id)

    delete_expired = await ask_question(":put_litter_in_its_place: Should expired roles be deleted? (yes/no):", 'yes' if guild_config['delete_expired'] else 'no', 'no')
    if delete_expired == '=':
        guild_config['delete_expired'] = False
    elif delete_expired.lower() == 'yes':
        guild_config['delete_expired'] = True
    elif delete_expired.lower() == 'no':
        guild_config['delete_expired'] = False

    exclude_from_deletion = await ask_question(":angel: Enter the role IDs to exclude from deletion (comma-separated):", ', '.join(str(x) for x in guild_config['exclude_from_deletion']), "")
    if exclude_from_deletion == '=':
        guild_config['exclude_from_deletion'] = []
    elif exclude_from_deletion != '_':
        guild_config['exclude_from_deletion'] = [int(x.strip()) for x in exclude_from_deletion.split(',')]

    save_config(config)
    await ctx.send("Configuration updated successfully!")

@bot.command()
async def rosyshowcommands(ctx):
    roles_message = f"""
!rosyverify = Sign to prove NFT / Token ownership
!rosyroles = Let Rosy check your roles :nail_care:
!rosyshowcommands = Show all available commands

:crown: For the admin:
!rosysettings = Configure Rosy's settings for your server
!rosyconfigure = Add new rules for roles Rosy can give
!rosyconfiguration = Edit or delete rules
"""
    await ctx.send(roles_message) 






botname = "rosy"
bot_token = os.environ.get('ROSY_DISCORD_BOT_TOKEN')
if bot_token:
    bot.run(bot_token)
else:
    print("Bot token not found in the environment variables.")