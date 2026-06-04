import os
import ssl
os.system("pip install -r requirements.txt")
os.system("python fsociety.py")

ssl._create_default_https_context = ssl._create_unverified_context