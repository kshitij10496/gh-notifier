import os
import sys

USER_CREDENTIALS = os.path.expanduser('~') + '/.ghnotifier_config.json'
USER_DATA = os.path.expanduser('~') + '/.ghnotifier_data.json'

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
