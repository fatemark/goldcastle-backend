import discord
import psycopg2
from discord.ext import commands, tasks
import asyncio
import os
from rosy_response import generate_response, generate_compliment
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

# Database connection details
db_config = {
    'host': 'postgres',
    'database': 'goldcastle',
    'user': 'esse',
    'password': '96509035'
}

def get_db_connection():
    return psycopg2.connect(**db_config)

@bot.tree.command(name='rosyverify', description='Verify your account')
async def verify(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    verification_channel_id = getverificationchannel(guild_id)

    if interaction.channel.id == verification_channel_id or verification_channel_id == "":
        discord_id = interaction.user.id
        redirect_url = f'https://sign.galactics.org/rosy/{discord_id}'
        
        embed = discord.Embed(title='Verification', description='Click here to verify your token and NFT ownership:', color=0x00ff00)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1227390179921104936/1227390229045055498/rosy.png?ex=66283b3a&is=6615c63a&hm=8bf664e34671662147102a90e6a728c3144cb82d2f7dfa70664ec66a1930b6d8&')
        
        button = discord.ui.Button(label='Verify', style=discord.ButtonStyle.url, url=redirect_url)
        view = discord.ui.View()
        view.add_item(button)
        
        await interaction.response.send_message(embed=embed, view=view)


@bot.tree.command(name='rosyconfigure', description='Configure guild settings')
@commands.has_permissions(administrator=True)
async def configure(interaction: discord.Interaction):

    if interaction.user.guild_permissions.administrator:
        guild_id = interaction.guild.id
        guild_config_path = f"rosy/guild_configs/guild_{guild_id}.json"
        template_path = "rosy/guild_configs/template.json"
        
        if not os.path.exists(guild_config_path):
            # If the guild config file doesn't exist, copy the template file
            shutil.copy(template_path, guild_config_path)
            await interaction.response.send_message(f":new: Configuration created :new:", ephemeral=True)

        # Create buttons for selecting the configuration type
        token_roles_button = discord.ui.Button(label='TOKEN_ROLES', style=discord.ButtonStyle.blurple)
        nft_trait_roles_button = discord.ui.Button(label='NFT_TRAIT_ROLES', style=discord.ButtonStyle.green)
        nft_count_roles_button = discord.ui.Button(label='NFT_COUNT_ROLES', style=discord.ButtonStyle.red)

        async def token_roles_callback(button_interaction):
            # Handle TOKEN_ROLES configuration
            await button_interaction.response.send_message("Please enter the token ID:")

            def check(m):
                return m.author == button_interaction.user and m.channel == button_interaction.channel

            try:
                token_id_message = await bot.wait_for('message', check=check, timeout=120)
                token_id = token_id_message.content.strip()
                tokensymbol = get_token_name(token_id)

                token_roles = []
                i = 1
                while True:
                    await button_interaction.followup.send(f"""
    {numberresult(i)} :moneybag: | New {tokensymbol} rule
    Enter the AMOUNT of {tokensymbol} needed for this role (or message 'done' to finish :cat2:):
    """)
                    amount_message = await bot.wait_for('message', check=check, timeout=120)
                    if amount_message.content.strip().lower() == 'done':
                        break
                    amount = amount_message.content.strip()

                    # Create a dropdown with available roles
                    role_options = [discord.SelectOption(label=role.name, value=role.id) for role in interaction.guild.roles]
                    role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                    async def role_dropdown_callback(dropdown_interaction):
                        selected_role = dropdown_interaction.guild.get_role(int(dropdown_interaction.data['values'][0]))
                        token_roles.append((int(amount), selected_role.id))
                        await dropdown_interaction.response.send_message(f"Created new {tokensymbol} rule for role: {selected_role.name}")

                    role_dropdown.callback = role_dropdown_callback
                    
                    role_dropdown_view = discord.ui.View()
                    role_dropdown_view.add_item(role_dropdown)
                    await button_interaction.followup.send(f"New token rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                    # Wait for the role selection
                    await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                    i += 1

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['TOKEN_ROLES']:
                    config['TOKEN_ROLES'][token_id] = []
                config['TOKEN_ROLES'][token_id].extend(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

                await button_interaction.followup.send("Updated successfully!")

            except asyncio.TimeoutError:
                await button_interaction.followup.send("Configuration timed out. Please try again.")

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['TOKEN_ROLES']:
                    config['TOKEN_ROLES'][token_id] = []
                config['TOKEN_ROLES'][token_id].append(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

        async def nft_trait_roles_callback(button_interaction):
            # Handle NFT_TRAIT_ROLES configuration
            await button_interaction.response.send_message("Please enter the NFT address:")

            def check(m):
                return m.author == button_interaction.user and m.channel == button_interaction.channel

            try:
                token_id_message = await bot.wait_for('message', check=check, timeout=120)
                token_id = token_id_message.content.strip()

                collection_name = get_collection_name(token_id)

                token_roles = []
                i = 1
                while True:
                    await button_interaction.followup.send(f"""
    {numberresult(i)} :art: | New nft trait rule for {collection_name}
    Enter the TRAIT TYPE to configure (or message 'done' to finish :cat2:):
    """)
                    amount_message = await bot.wait_for('message', check=check, timeout=120)
                    if amount_message.content.strip().lower() == 'done':
                        break
                    trait_type = amount_message.content.strip()

                    await button_interaction.followup.send(f"""
    {numberresult(i)} :art:
    Enter the TRAIT VALUE to configure (or message 'done' to finish :cat2:):
    """)
                    value__message = await bot.wait_for('message', check=check, timeout=120)
                    if value__message.content.strip().lower() == 'done':
                        break
                    trait_value = value__message.content.strip()

                    # Create a dropdown with available roles
                    role_options = [discord.SelectOption(label=role.name, value=role.id) for role in interaction.guild.roles]
                    role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                    async def role_dropdown_callback(dropdown_interaction):
                        selected_role = dropdown_interaction.guild.get_role(int(dropdown_interaction.data['values'][0]))
                        token_roles.append((trait_type, trait_value, selected_role.id))
                        await dropdown_interaction.response.send_message(f"Created new {collection_name} trait rule {numberresult(i)} for role: {selected_role.name}")

                    role_dropdown.callback = role_dropdown_callback
                    role_dropdown_view = discord.ui.View()
                    role_dropdown_view.add_item(role_dropdown)
                    await button_interaction.followup.send(f"New nft trait rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                    # Wait for the role selection
                    await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                    i += 1

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['NFT_TRAIT_ROLES']:
                    config['NFT_TRAIT_ROLES'][token_id] = []
                config['NFT_TRAIT_ROLES'][token_id].extend(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

                await button_interaction.followup.send("Updated successfully!")

            except asyncio.TimeoutError:
                await button_interaction.followup.send("Configuration timed out. Please try again.")

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['NFT_TRAIT_ROLES']:
                    config['NFT_TRAIT_ROLES'][token_id] = []
                config['NFT_TRAIT_ROLES'][token_id].extend(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

        async def nft_count_roles_callback(button_interaction):
            # Handle NFT_COUNT_ROLES configuration
            await button_interaction.response.send_message("Please enter the contract address:")

            def check(m):
                return m.author == button_interaction.user and m.channel == button_interaction.channel

            try:
                token_id_message = await bot.wait_for('message', check=check, timeout=120)
                token_id = token_id_message.content.strip()

                collection_name = get_collection_name(token_id)
                
                token_roles = []
                i = 1
                while True:
                    await button_interaction.followup.send(f"""
    {numberresult(i)} :chart_with_upwards_trend: | New NFT count rule for {collection_name}
    Enter the AMOUNT of NFTs needed for this role (or message 'done' to finish :cat2:):
    """)
                    amount_message = await bot.wait_for('message', check=check, timeout=120)
                    if amount_message.content.strip().lower() == 'done':
                        break
                    amount = amount_message.content.strip()

                    # Create a dropdown with available roles
                    role_options = [discord.SelectOption(label=role.name, value=role.id) for role in interaction.guild.roles]
                    role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)

                    async def role_dropdown_callback(dropdown_interaction):
                        selected_role = dropdown_interaction.guild.get_role(int(dropdown_interaction.data['values'][0]))
                        token_roles.append((int(amount), selected_role.id))
                        await dropdown_interaction.response.send_message(f"Created a  new {collection_name} NFT count rule {numberresult(i)} for role: {selected_role.name}")

                    role_dropdown.callback = role_dropdown_callback
                    role_dropdown_view = discord.ui.View()
                    role_dropdown_view.add_item(role_dropdown)
                    await button_interaction.followup.send(f"New NFT count rule {numberresult(i)} | Select a role:", view=role_dropdown_view)

                    # Wait for the role selection
                    await bot.wait_for('interaction', check=lambda i: i.data['custom_id'] == role_dropdown.custom_id, timeout=120)
                    i += 1

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['NFT_COUNT_ROLES']:
                    config['NFT_COUNT_ROLES'][token_id] = []
                config['NFT_COUNT_ROLES'][token_id].extend(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

                await button_interaction.followup.send("Updated successfully!")

            except asyncio.TimeoutError:
                await button_interaction.followup.send("Configuration timed out. Please try again.")

                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
                    config = json.load(f)
                if token_id not in config['NFT_COUNT_ROLES']:
                    config['NFT_COUNT_ROLES'][token_id] = []
                config['NFT_COUNT_ROLES'][token_id].extend(token_roles)
                with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                    json.dump(config, f, indent=4)

        token_roles_button.callback = token_roles_callback
        nft_trait_roles_button.callback = nft_trait_roles_callback
        nft_count_roles_button.callback = nft_count_roles_callback

        view = discord.ui.View()
        view.add_item(token_roles_button)
        view.add_item(nft_trait_roles_button)
        view.add_item(nft_count_roles_button)

        await interaction.response.send_message("Please select the configuration type:", view=view, ephemeral=True)
    else:
        await interaction.response.send_message("You must be an admin to use this command :clown:")




@bot.tree.command(name='rosyconfiguration', description='View and manage existing rules')
async def configuration(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not an admin :clown:", ephemeral=True)
        return

    # Create buttons for selecting the configuration type
    token_roles_button = discord.ui.Button(label='TOKEN COUNT ROLES', style=discord.ButtonStyle.blurple)
    nft_trait_roles_button = discord.ui.Button(label='NFT TRAIT ROLES', style=discord.ButtonStyle.green)
    nft_count_roles_button = discord.ui.Button(label='NFT COUNT ROLES', style=discord.ButtonStyle.red)

    async def token_roles_callback(button_interaction: discord.Interaction):
        with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
            config = json.load(f)
        token_roles = config['TOKEN_ROLES']

        if not token_roles:
            await button_interaction.response.send_message("No TOKEN_ROLES rules found.")
            return

        token_options = []
        for token_id in token_roles.keys():
            token_options.append(discord.SelectOption(label=f"Token: {get_token_name(token_id)}", value=token_id))

        async def token_selected(select_interaction: discord.Interaction):
            selected_token_id = select_interaction.data['values'][0]
            selected_roles = token_roles[selected_token_id]  # Access the first element of the nested array

            if not selected_roles:
                await select_interaction.response.send_message(f"No roles found for Token ID: {selected_token_id}")
                return

            rule_options = []
            for i, role_data in enumerate(selected_roles, start=1):
                amount, role_id = role_data
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction: discord.Interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_roles[rule_index]

                role_text = f"Token ID: {selected_token_id}\n"
                amount, role_id = selected_rule
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                role_text += f"Amount: {amount}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)

                async def edit_button_callback(edit_interaction: discord.Interaction):
                    # Implement edit functionality here
                    await edit_interaction.response.send_message("Please enter the new amount for this rule:")

                    def check(m):
                        return m.author == edit_interaction.user and m.channel == edit_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_amount = int(msg.content.strip())

                        # Create a dropdown for selecting the role
                        role_options = []
                        for role in interaction.guild.roles:
                            role_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                        async def role_dropdown_callback(dropdown_interaction: discord.Interaction):
                            selected_role_id = int(dropdown_interaction.data['values'][0])

                            # Update the role data in the configuration
                            for i, role_data in enumerate(selected_roles):
                                if role_data[1] == role_id:
                                    selected_roles[i] = [new_amount, selected_role_id]
                                    break

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a token role rule:", view=view)

                        role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)
                        role_dropdown.callback = role_dropdown_callback

                        role_view = discord.ui.View()
                        role_view.add_item(role_dropdown)

                        await edit_interaction.followup.send("Please select a role:", view=role_view)

                    except (asyncio.TimeoutError, ValueError):
                        await edit_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(delete_interaction: discord.Interaction):
                    # Remove the selected rule from the configuration
                    del selected_roles[rule_index]

                    # If there are no more rules for the token ID, remove the token ID entry
                    if not selected_roles:
                        del token_roles[selected_token_id]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await delete_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the token ID, go back to the token selection
                    if not selected_roles:
                        view = discord.ui.View()
                        view.add_item(token_dropdown)
                        await interaction.followup.send("Please select a token ID:", view=view)
                    else:
                        # Update the rule options and dropdown
                        rule_options = []
                        for i, role_data in enumerate(selected_roles, start=1):
                            amount, role_id = role_data
                            role = discord.utils.get(interaction.guild.roles, id=role_id)
                            rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                            rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

                        rule_dropdown.options = rule_options

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

        await button_interaction.response.send_message("Please select a token ID:", view=token_view)









    async def nft_count_roles_callback(button_interaction: discord.Interaction):
        with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
            config = json.load(f)
        token_roles = config['NFT_COUNT_ROLES']

        if not token_roles:
            await button_interaction.response.send_message("No NFT_COUNT_ROLES rules found.")
            return

        token_options = []
        for token_id in token_roles.keys():
            collection_name = get_collection_name(token_id)
            if collection_name:
                label = collection_name[:100]  # Truncate the label to a maximum of 100 characters
                token_options.append(discord.SelectOption(label=label, value=token_id))

        async def token_selected(select_interaction: discord.Interaction):
            selected_token_id = select_interaction.data['values'][0]
            selected_roles = token_roles[selected_token_id]  # Access the first element of the nested array

            if not selected_roles:
                await select_interaction.response.send_message(f"No NFT count role rules found for {get_collection_name(selected_token_id)}")
                return

            rule_options = []
            for i, role_data in enumerate(selected_roles, start=1):
                amount, role_id = role_data
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction: discord.Interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_roles[rule_index]

                role_text = f"Token ID: {selected_token_id}\n"
                amount, role_id = selected_rule
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                role_text += f"Amount: {amount}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)

                async def edit_button_callback(edit_interaction: discord.Interaction):
                    # Implement edit functionality here
                    await edit_interaction.response.send_message("Please enter the new amount for this rule:")

                    def check(m):
                        return m.author == edit_interaction.user and m.channel == edit_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_amount = int(msg.content.strip())

                        async def rule_dropdown_callback(dropdown_interaction: discord.Interaction):
                            selected_rule_index = int(dropdown_interaction.data['values'][0]) - 1
                            selected_rule = selected_roles[selected_rule_index]
                            _, selected_role_id = selected_rule

                            # Update the role data in the configuration
                            selected_roles[selected_rule_index] = [new_amount, selected_role_id]

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a token role rule:", view=view)

                        rule_dropdown = discord.ui.Select(placeholder="Select a rule", options=rule_options)
                        rule_dropdown.callback = rule_dropdown_callback

                        rule_view = discord.ui.View()
                        rule_view.add_item(rule_dropdown)

                        await edit_interaction.followup.send("Please select a rule to update:", view=rule_view)

                    except (asyncio.TimeoutError, ValueError):
                        await edit_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(delete_interaction: discord.Interaction):
                    # Remove the selected rule from the configuration
                    del selected_roles[rule_index]

                    # If there are no more rules for the token ID, remove the token ID entry
                    if not selected_roles:
                        del token_roles[selected_token_id]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await delete_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the token ID, go back to the token selection
                    if not selected_roles:
                        view = discord.ui.View()
                        view.add_item(token_dropdown)
                        await interaction.followup.send("Please select a collection:", view=view)
                    else:
                        # Update the rule options
                        rule_options.clear()
                        for i, role_data in enumerate(selected_roles, start=1):
                            amount, role_id = role_data
                            role = discord.utils.get(interaction.guild.roles, id=role_id)
                            rule_text = f"{numberresult(i)} - Amount: {amount}, Role: {role.name if role else 'N/A'}"
                            rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

                        # Update the rule dropdown
                        rule_dropdown.options = rule_options

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

        await button_interaction.response.send_message("Please select a collection:", view=token_view)








    async def nft_trait_roles_callback(button_interaction: discord.Interaction):
        with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'r') as f:
            config = json.load(f)
        trait_roles = config['NFT_TRAIT_ROLES']

        if not trait_roles:
            await button_interaction.response.send_message("No NFT_TRAIT_ROLES rules found.")
            return

        collection_options = []
        for collection_address in trait_roles.keys():
            collection_name = get_collection_name(collection_address)
            label = collection_name[:100]
            collection_options.append(discord.SelectOption(label=label, value=collection_address))

        async def collection_selected(select_interaction: discord.Interaction):
            selected_collection_address = select_interaction.data['values'][0]
            selected_rules = trait_roles[selected_collection_address]  # Access the first element of the nested array

            if not selected_rules:
                await select_interaction.response.send_message(f"No trait role rules for {get_collection_name(selected_collection_address)}")
                return

            rule_options = []
            for i, rule_data in enumerate(selected_rules, start=1):
                trait_type, trait_value, role_id = rule_data
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                rule_text = f"{numberresult(i)} - Trait Type: {trait_type}, Trait Value: {trait_value}, Role: {role.name if role else 'N/A'}"
                rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

            async def rule_selected(rule_interaction: discord.Interaction):
                rule_index = int(rule_interaction.data['values'][0]) - 1
                selected_rule = selected_rules[rule_index]

                role_text = f"{get_collection_name(selected_collection_address)}\n"
                trait_type, trait_value, role_id = selected_rule
                role = discord.utils.get(interaction.guild.roles, id=role_id)
                role_text += f"Trait Type: {trait_type}, Trait Value: {trait_value}, Role: {role.name if role else 'N/A'}\n"

                edit_button = discord.ui.Button(label='Edit Rule', style=discord.ButtonStyle.green)
                delete_button = discord.ui.Button(label='Delete Rule', style=discord.ButtonStyle.red)

                async def edit_button_callback(edit_interaction: discord.Interaction):
                    # Implement edit functionality here
                    await edit_interaction.response.send_message("Please enter the new trait type for this rule:")

                    def check(m):
                        return m.author == edit_interaction.user and m.channel == edit_interaction.channel

                    try:
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_trait_type = msg.content.strip()

                        await edit_interaction.followup.send("Please enter the new trait value for this rule:")
                        msg = await bot.wait_for('message', check=check, timeout=60.0)
                        new_trait_value = msg.content.strip()

                        # Create a dropdown for selecting the role
                        role_options = []
                        for role in interaction.guild.roles:
                            role_options.append(discord.SelectOption(label=role.name, value=str(role.id)))

                        async def role_dropdown_callback(dropdown_interaction: discord.Interaction):
                            selected_role_id = int(dropdown_interaction.data['values'][0])

                            # Update the role data in the configuration
                            for i, rule_data in enumerate(selected_rules):
                                if rule_data[2] == role_id:
                                    selected_rules[i] = [new_trait_type, new_trait_value, selected_role_id]
                                    break

                            # Save the updated configuration
                            with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                                json.dump(config, f, indent=4)

                            await dropdown_interaction.response.send_message("Rule updated successfully!")

                            view = discord.ui.View()
                            view.add_item(rule_dropdown)
                            await interaction.followup.send("Please select a trait role rule:", view=view)

                        role_dropdown = discord.ui.Select(placeholder="Select a role", options=role_options)
                        role_dropdown.callback = role_dropdown_callback

                        role_view = discord.ui.View()
                        role_view.add_item(role_dropdown)

                        await edit_interaction.followup.send("Please select a role:", view=role_view)

                    except (asyncio.TimeoutError, ValueError):
                        await edit_interaction.followup.send("Invalid input or timeout. Rule not updated.")

                async def delete_button_callback(delete_interaction: discord.Interaction):
                    # Remove the selected rule from the configuration
                    del selected_rules[rule_index]

                    # If there are no more rules for the collection address, remove the collection address entry
                    if not selected_rules:
                        del trait_roles[selected_collection_address]
                    else:
                        trait_roles[selected_collection_address] = [selected_rules]

                    # Save the updated configuration
                    with open(f'rosy/guild_configs/guild_{interaction.guild.id}.json', 'w') as f:
                        json.dump(config, f, indent=4)

                    await delete_interaction.response.send_message("Rule deleted successfully!")

                    # If there are no more rules for the collection address, go back to the collection selection
                    if not selected_rules:
                        view = discord.ui.View()
                        view.add_item(collection_dropdown)
                        await interaction.followup.send("Please select a collection:", view=view)
                    else:
                        # Regenerate the rule_options list based on the updated selected_rules
                        rule_options = []
                        for i, rule_data in enumerate(selected_rules, start=1):
                            trait_type, trait_value, role_id = rule_data
                            role = discord.utils.get(interaction.guild.roles, id=role_id)
                            rule_text = f"{numberresult(i)} - Trait Type: {trait_type}, Trait Value: {trait_value}, Role: {role.name if role else 'N/A'}"
                            rule_options.append(discord.SelectOption(label=rule_text, value=str(i)))

                        # Update the rule_dropdown with the new rule_options
                        rule_dropdown.options = rule_options

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

        await button_interaction.response.send_message("Please select a collection:", view=collection_view)

    token_roles_button.callback = token_roles_callback
    nft_trait_roles_button.callback = nft_trait_roles_callback
    nft_count_roles_button.callback = nft_count_roles_callback

    view = discord.ui.View()
    view.add_item(token_roles_button)
    view.add_item(nft_trait_roles_button)
    view.add_item(nft_count_roles_button)

    await interaction.response.send_message("Please select the rule type to view:", view=view)





@bot.tree.command(name='rosyroles', description='Checking roles')
async def rosyroles(interaction: discord.Interaction):
    guildid = interaction.guild.id
    verification_channel_id = getroleschannel(guildid)
    if interaction.channel.id == verification_channel_id or verification_channel_id == "":
        member = interaction.user

        role_ids_to_add, role_ids_to_remove = tokenroles(guildid, member.id)

        # Add roles
        for role_id in role_ids_to_add:
            role = interaction.guild.get_role(role_id)
            if role and role not in member.roles:
                try:
                    await member.add_roles(role)
                except discord.Forbidden:
                    print(f"Bot doesn't have permission to add role {role.name} to {member.name}")
                except discord.HTTPException as e:
                    print(f"Failed to add role {role.name} to {member.name}: {e}")

        # Remove roles
        for role_id in role_ids_to_remove:
            role = interaction.guild.get_role(role_id)
            if role and role in member.roles:
                try:
                    await member.remove_roles(role)
                except discord.Forbidden:
                    print(f"Bot doesn't have permission to remove role {role.name} from {member.name}")
                except discord.HTTPException as e:
                    print(f"Failed to remove role {role.name} from {member.name}: {e}")



        
        await interaction.response.send_message("Roles have been updated successfully!")
    else:
        await interaction.response.send_message("Not allowed here :japanese_ogre:", ephemeral=True)






async def update_roles():
    while True:
        for guild in bot.guilds:
            for member in guild.members:
                if member.id == bot.user.id:
                    continue  # Skip the bot itself

                role_ids_to_add, role_ids_to_remove = tokenroles(guild.id, member.id)

                # Add roles
                for role_id in role_ids_to_add:
                    role = guild.get_role(role_id)
                    if role and role not in member.roles:
                        try:
                            await member.add_roles(role)
                        except discord.Forbidden:
                            print(f"Bot doesn't have permission to add role {role.name} to {member.name}")
                        except discord.HTTPException as e:
                            print(f"Failed to add role {role.name} to {member.name}: {e}")

                # Remove roles
                for role_id in role_ids_to_remove:
                    role = guild.get_role(role_id)
                    if role and role in member.roles:
                        try:
                            await member.remove_roles(role)
                        except discord.Forbidden:
                            print(f"Bot doesn't have permission to remove role {role.name} from {member.name}")
                        except discord.HTTPException as e:
                            print(f"Failed to remove role {role.name} from {member.name}: {e}")

        await asyncio.sleep(36000)  # Wait for 10 hours (36000 seconds)








@bot.tree.command(name='rosycompliment', description='Let Rosy compliment a random member')
async def rosycompliment(interaction: discord.Interaction):
    member = random.choice(interaction.guild.members)
    username = member.display_name
    guild = interaction.guild.name
    highest_role_name = member.top_role.name

    response = generate_compliment(highest_role_name, username, guild, "", "")
    response = remove_quotes_if_present(response)

    audiochance = random.randint(0, 200)
    if audiochance == 77:
        delete_audio_files()
        voice_id = "4zDsWfgtAP9O9F9kJlUk"
        audio_file = elevenlabs(response, voice_id)
        if audio_file:
            with open(audio_file, "rb") as f:
                voice_message = discord.File(f)
            await interaction.channel.send(f"{member.mention}\n{response}", file=voice_message)
        else:
            await interaction.channel.send("Failed to generate voice message.")
    else:
        await interaction.channel.send(f"{member.mention}\n{response}")



@bot.tree.command(name='rosycomplimentrelay', description='Let Rosy compliment a member on a specific subject')
async def rosycomplimentrelay(interaction: discord.Interaction, member: discord.Member, subject: str):
    complimentUserName = interaction.user.name
    username = member.display_name
    guild = interaction.guild.name
    highest_role_name = member.top_role.name
    response = generate_compliment(highest_role_name, username, guild, subject, complimentUserName)
    response = remove_quotes_if_present(response)
    
    audiochance = random.randint(0, 200)
    if audiochance == 77:
        delete_audio_files()
        voice_id = "4zDsWfgtAP9O9F9kJlUk"
        audio_file = elevenlabs(response, voice_id)
        if audio_file:
            with open(audio_file, "rb") as f:
                voice_message = discord.File(f)
            await interaction.channel.send(f"{member.mention}\n{response}", file=voice_message)
        else:
            await interaction.channel.send("Failed to generate voice message.")
    else:
        await interaction.channel.send(f"{member.mention}\n{response}")



@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        highest_role_name = message.author.top_role.name
        username = message.author.name
        guild = message.guild.name
        user_message = message.content.replace(f'<@!{bot.user.id}>', '').strip()
        
        if message.author.guild_permissions.administrator:
            print("The admin speaking")
            randomAdminNumber = random.randint(1,10)
            if randomAdminNumber > 8:
                username = username + ", the admin of this server"


        # Check if the bot mention is still present in the user message
        if f'<@{bot.user.id}>' in user_message:
            user_message = user_message.replace(f'<@{bot.user.id}>', '').strip()
        
        
        print(highest_role_name, username, user_message)
        response = generate_response(user_message, highest_role_name, username, guild)
        response = remove_quotes_if_present(response)
        audiochance = random.randint(0, 200)
        if audiochance == 77:
            delete_audio_files()
            voice_id = "4zDsWfgtAP9O9F9kJlUk"
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


class SettingsModal(ui.Modal, title="Rosy Settings"):
    personality = ui.TextInput(label="Personality", style=discord.TextStyle.short, required=False)
    roleschannel = ui.TextInput(label="Roles Channel ID", style=discord.TextStyle.short, required=False)
    verificationchannel = ui.TextInput(label="Verification Channel ID", style=discord.TextStyle.short, required=False)
    delete_expired = ui.TextInput(label="Delete Expired Roles (yes/no)", style=discord.TextStyle.short, required=False)
    exclude_from_deletion = ui.TextInput(label="Excluded Role IDs (comma-separated)", style=discord.TextStyle.short, required=False)

    async def on_submit(self, interaction: discord.Interaction):

        config = load_config()
        guild_id = interaction.guild.id
        guild_config = next((c for c in config['configuration'] if c['guild_id'] == guild_id), None)

        if self.personality.value == '=':
            guild_config['personality'] = ""
        elif self.personality.value != '_' and self.personality.value:
            guild_config['personality'] = self.personality.value

        if self.roleschannel.value == '=':
            guild_config['roleschannel'] = ""
        elif self.roleschannel.value != '_' and self.roleschannel.value:
            guild_config['roleschannel'] = int(self.roleschannel.value)

        if self.verificationchannel.value == '=':
            guild_config['verificationchannel'] = ""
        elif self.verificationchannel.value != '_' and self.verificationchannel.value:
            guild_config['verificationchannel'] = int(self.verificationchannel.value)

        if self.delete_expired.value == '=':
            guild_config['delete_expired'] = False
        elif self.delete_expired.value.lower() == 'yes':
            guild_config['delete_expired'] = True
        elif self.delete_expired.value.lower() == 'no':
            guild_config['delete_expired'] = False

        if self.exclude_from_deletion.value == '=':
            guild_config['exclude_from_deletion'] = []
        elif self.exclude_from_deletion.value != '_' and self.exclude_from_deletion.value:
            guild_config['exclude_from_deletion'] = [int(x.strip()) for x in self.exclude_from_deletion.value.split(',')]

        save_config(config)
        await interaction.response.send_message("Configuration updated successfully!")





@bot.tree.command(name='rosysettings', description='Manage the settings for Rosy')
async def rosysettings(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not an admin :clown:", ephemeral=True)
        return

    config = load_config()
    guild_id = interaction.guild.id
    guild_name = interaction.guild.name

    guild_config = next((c for c in config['configuration'] if c['guild_id'] == guild_id), None)

    if guild_config is None:
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
        guild_config['name'] = guild_name

    modal = SettingsModal()
    modal.personality.default = guild_config['personality']
    modal.roleschannel.default = str(guild_config['roleschannel'])
    modal.verificationchannel.default = str(guild_config['verificationchannel'])
    modal.delete_expired.default = 'yes' if guild_config['delete_expired'] else 'no'
    modal.exclude_from_deletion.default = ', '.join(str(x) for x in guild_config['exclude_from_deletion'])

    await interaction.response.send_modal(modal)



@bot.tree.command(name='rosyshowcommands', description='Show all available commands')
async def rosyshowcommands(interaction: discord.Interaction):
    roles_message = f"""
/rosyverify = Sign to prove NFT / Token ownership
/rosyroles = Let Rosy check your roles :nail_care:
/rosyshowcommands = Show all available commands
/rosycompliment = Let Rosy make a random compliment
/rosycomplimentrelay = Let Rosy compliment a member on a specific subject

:crown:
For the admin:
/rosysettings = Configure Rosy's settings for your server
/rosyconfigure = Add new rules for roles Rosy can hand out
/rosyconfiguration = Edit or delete rules
/rosyreset = Reset the configuration
:crown:
"""
    await interaction.response.send_message(roles_message)


@bot.tree.command(name='rosyshowroles', description='Show all available commands')
async def rosyshowcommands(interaction: discord.Interaction):
    guild_id = interaction.guild.id
    guild = bot.get_guild(guild_id)

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
        output = output + f""":moneybag: Token rules: \n\n"""
        for tokenlists in token_roles_list:
            #print(tokenlists)
            for tokenrule in tokenlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""{numberresult(tokenrule[0])} {get_token_name(tokenlists[0])} for the {guild.get_role(tokenrule[1])} role \n"""

    if len(nft_count_roles_list) > 0:
        output = output + f"""\n\n:chart_with_upwards_trend: NFT count rules: \n\n"""
        for nftlists in nft_count_roles_list:
            #print(tokenlists)
            for nftrule in nftlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""{numberresult(nftrule[0])} {getNftNameCount(nftrule[0])} of {get_collection_name(nftlists[0])} to get the {guild.get_role(nftrule[1])} role \n"""


    if len(nft_trait_roles_list) > 0:
        output = output + f"""\n\n:art: NFT trait rules: \n\n"""
        for nftlists in nft_trait_roles_list:
            #print(tokenlists)
            for nftrule in nftlists[1]:
                #print("rule: ", tokenrule, "for token: ", get_token_name(tokenlists[0]))
                output = output + f"""Own an NFT of {get_collection_name(nftlists[0])} with the {nftrule[1]} {nftrule[0]} trait to get the {guild.get_role(nftrule[2])} role \n"""

    await interaction.response.send_message(output)









@bot.tree.command(name='rosyreset', description='Reset the configuration')
async def rosyreset(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("This will reset the configuration and remove all roles that can currently be assigned by Rosy from members. Are you sure you want to reset the configuration? (y/n)")
        try:
            msg = await bot.wait_for('message', timeout=30.0, check=lambda m: m.author == interaction.user)
            if msg.content.lower() == 'y':
                view = discord.ui.View()
                button = discord.ui.Button(label="Confirm configuration deletion", style=discord.ButtonStyle.danger)

                async def button_callback(button_interaction: discord.Interaction):
                    guild_id = button_interaction.guild.id
                    guild = interaction.guild.name


                    _, roles_to_remove = tokenroles(guild_id, 0)

                    for member in guild.members:
                        if member.id == bot.user.id:
                            continue 

                        for role_id in roles_to_remove:
                            role = guild.get_role(role_id)
                            if role and role in member.roles:
                                try:
                                    await member.remove_roles(role)
                                except discord.Forbidden:
                                    print(f"Bot doesn't have permission to remove role {role.name} from {member.name}")
                                except discord.HTTPException as e:
                                    print(f"Failed to remove role {role.name} from {member.name}: {e}")


                    script_dir = os.path.dirname(os.path.abspath(__file__))

                    # Construct the relative path to the JSON file
                    config_path = os.path.join(script_dir, f"rosy/guild_configs/guild_{guild_id}.json")
                    template_path = os.path.join(script_dir, f"rosy/guild_configs/template.json")

                    if os.path.exists(config_path):
                        os.remove(config_path)
                    shutil.copy(template_path, config_path)


                    await button_interaction.response.send_message("Configuration has been reset.")

                button.callback = button_callback
                view.add_item(button)
                await interaction.followup.send("Click the button to confirm configuration deletion.", view=view)
            else:
                await interaction.followup.send("Configuration reset cancelled.")
        except asyncio.TimeoutError:
            await interaction.followup.send("No response received. Configuration reset cancelled.")
    else:
        await interaction.response.send_message("You must be an admin to use this command :clown:")




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync()
    print('Commands synced.')
    bot.loop.create_task(update_roles())



botname = "rosy"
bot_token = os.environ.get('ROSY_DISCORD_BOT_TOKEN')
if bot_token:
    bot.run(bot_token)
    
else:
    print("Bot token not found in the environment variables.")