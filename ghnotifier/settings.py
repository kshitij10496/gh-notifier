import os
import sys

USER_CREDENTIALS = os.path.expanduser('~') + '/.ghnotifier_config.json'
USER_DATA = os.path.expanduser('~') + '/.ghnotifier_data.json'

PLATFORM = sys.platform

URL = 'https://api.github.com' 
HEADERS = {'Accept': 'application/vnd.github.v3+json'}
