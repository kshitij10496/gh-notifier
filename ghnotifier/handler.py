import os
import json

from userclass import User
from repo import Repo
from notification import Notification
from settings import USER_CREDENTIALS, USER_DATA, USERNAME, NOTIFIER

def dump_user_data(user):
    """ Function to store the User object in a JSON file.

    Parameters
    ==========
    user: User
        The object to be stored. 
    
    """
    # create the USER_DATA file if it does not already exist.
    with open(USER_DATA, 'w') as f:
        json.dump(user.toJSON(), f)

def load_user_data(user):
    with open(USER_DATA, 'r') as f:
        data = json.loads(json.load(f))
        if data['username'] == user.username:
            userdata = data
        else:
            print('Wrong input') 

    return userdata

def main_handler():
    newuser = User.from_handle(USERNAME) # New User Data
    
    if os.path.isfile(USER_DATA):
        userdata = load_user_data(newuser) # Old user data
    
    else:
        userdata = json.loads(User(USERNAME).toJSON())

    # get followers notification
    old_followers = userdata['followers']
    notifications = newuser.get_notifications(old_followers)
    
    # get repo notifications
    newrepos = newuser.repos
    oldrepos = userdata['repos']
    for newrepo in newrepos:
        if oldrepos is None:
            oldstars, oldwatchers, oldforks = 0, 0, 0
        else:
            for oldrepo in oldrepos:
                if newrepo.name == oldrepo['name']:
                    oldstars, oldwatchers, oldforks = oldrepo['stars'], oldrepo['watchers'], oldrepo['forks']
                    break
            else:
                oldstars, oldwatchers, oldforks = 0, 0, 0

        repo_notifications = newrepo.get_notifications(oldstars, oldwatchers, oldforks)
        # print("Repo: " + str(newrepo))

        notifications += repo_notifications
    
    for notification in notifications:
        #print(notification.message)
        notification.notify()

    dump_user_data(newuser)
