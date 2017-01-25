import os
import sys
import subprocess
import json
import getpass

USER_CREDENTIALS = os.path.expanduser('~') + '/.ghnotifier_config.json'
USER_DATA = os.path.expanduser('~') + '/.ghnotifier_data.json'

if os.path.isfile(USER_CREDENTIALS):
    with open(USER_CREDENTIALS) as f:
        CREDENTIALS = json.load(f)

    USERNAME = CREDENTIALS['USERNAME']
    PASSWORD = CREDENTIALS['PASSWORD']

else:
    USERNAME = input("Enter your GitHub username: ")
    PASSWORD = getpass.getpass(prompt="Enter your password: ")
    CREDENTIALS = {
                    "USERNAME": USERNAME,
                    "PASSWORD": PASSWORD 
                    }
            
    with open(USER_CREDENTIALS, 'w') as f:
        json.dump(CREDENTIALS, f)
    

PLATFORM = sys.platform
NOTIFIER = None
if PLATFORM == 'darwin':
    # test if terminal-notifier is present on the system or not
    status = subprocess.run(['which', 'terminal-notifier']).returncode
    if status == 0:
        NOTIFIER = "terminal-notifier"
    else:
        print("Kindly install terminal-notifier for MacOS.") # Raise exception
elif PLATFORM == 'linux':
    NOTIFIER = "notify-send"

else:
    print("Your system is not supported yet.") # Raise exception
        
URL = 'https://api.github.com' 
HEADERS = {'Accept': 'application/vnd.github.v3+json'}
