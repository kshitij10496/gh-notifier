import os
import subprocess
import json

from github import Github
from settings import USERNAME, PASSWORD

g = Github(USERNAME, PASSWORD)

user = g.get_user()

# create a data storage file
file = os.path.expanduser('~') + '/.ghnotifier'

try:
    with open(file, 'r') as fp:
        data = json.load(fp)

except FileNotFoundError:
    with open(file, 'w') as fp:
        data = {
                USERNAME : {
                            "followers": 0,
                            "repos": []
                            }
                }
        json.dump(data, fp)

def notify(message):
    platform = sys.platform
    title = "GitHub Notification"
    if platform == 'darwin':
        status = subprocess.run(["which", "terminal-notifier"]).returncode
        if status == 0:
            subprocess.run(["terminal-notifier", "-title", "GitHub Notification", "-message", "kshitij10496", "-timeout", 10])

        else:
            print("Kindly install terminal-notifier for MacOS.")
            return -1

def logic(current_data, previous_data, context=None):
    number_of_new_followers = current_data -  previous_data
    if( previous_data == 0): # no change in following
        return 0

    elif( previous_data > 0): # new followers
        for follower in user.get_followers[previous_data:]:
            status = notify("{} {}ed {}".format(follower.name, *context))

        return 1

    else: # people unfollowed
        # update DB
        notify("{} users un{}ed {}".format(number_of_new_followers, *context))
        return -1

# handle user's followers updates
def user_followers():
    current_followers = user.followers
    user_data = data[user.login]
    if "followers" in user_data:
        previous_followers = user_data["followers"]    
    else:
        previous_followers = 0

    user_data["followers"] = current_data
    return logic(current_followers, previous_followers, context=("follow", "you"))

# handle user's repo updates
def user_repos():
    user_data = data[user.login]
    for i in user.get_repos():
        name = i.name
        if "repos" in user_data["repos"]:
            repos = user_data["repos"]
        else:
            repos = user_data["repos"] = []

        repo = None
        repo = [repo for repo in repos if repo["name"] == name][0]
        if repo == None:
            repo["name"] = name
            previous_forks = 0
            previous_stars = 0
            previous_watchers = 0

        previous_forks = repo["forks"]
        previous_stars = repo["stars"]
        previous_watchers = repo["watchers"]
       
        repo["forks"] = current_forks = i.forks_count
        repo["stars"] = current_stars = i.stargazers_count
        repo["watchers"] = current_watchers = i.watchers_count

        logic(current_stars, previous_stars, context=("starr", name)) # past tense
        logic(current_watchers, previous_watchers, context=("watch", name))
        logic(current_forks, previous_forks, context=("fork", name))
        return 0
