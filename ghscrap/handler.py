import os
import json
import getpass

from github import Github

from notifier import notify, generate_message

USER_CREDENTIALS = os.path.expanduser('~') + '/.ghnotifier_config'
USER_DATA = os.path.expanduser('~') + '/.ghnotifier_data'

def create_user():

    # read/create a configuration file for user credentials
    try:
        with open(USER_DATA, 'r') as f:
            credentials = json.load(f)

    except FileNotFoundError:
        with open(USER_DATA, 'w') as f:
            USERNAME = input("Enter your GitHub username: ")
            PASSWORD = getpass.getpass(prompt="Enter your password: ")
            # store the credentials
            credentials = {
                    "USERNAME": USERNAME,
                    "PASSWORD": PASSWORD 
                    }
            json.dump(credentials, f)

    # create a data file if it does not already exist.
    try:
        with open(file, 'r') as fp:
            pass

    except FileNotFoundError:
        with open(file, 'w') as fp:
            # Schema for user data
            data = {
                    credentials["USERNAME"]:
                        {
                            "followers": 0;
                            "repos": []
                        }
                    }
            json.dump(data, fp)

    g = Github(credentials["USERNAME"], credentials["PASSWORD"])
    user = g.get_user()
    return user

def main_handler():
    user = create_user()
    # get user_data
    followers_status = handle_followers(user_data["followers"], user)
    user_data["followers"] = user.followers

    for repo in user.get_repos():
        updated_data = handle_repo(user_data["repos"], repo)
        user_data = updated_data

    with open(file, 'w') as fp:
        json.dump(updated_data, fp)


def logic(current_data, previous_data, context=None):
    delta = current_data - previous_data
    if delta == 0:
        return 0

    elif delta > 0:
        message = generate_message(delta, context, 1)

    else:
        message = generate_message(delta, context, -1)

    return notify(message)

# handle user's followers updates
def handle_followers(user_followers, user):
    previous_followers = user_followers
    user_followers = current_followers = user.followers
    context = ("follow", user.login)

    number_of_new_followers = current_followers - previous_followers
    if(number_of_new_followers == 0): # no change in following
        return 0

    elif(number_of_new_followers > 0): # new followers
        for follower in user.get_followers()[previous_followers:]:
            message = generate_message(follower.name, context, 1)
            notify(message)

        return 1

    else: # people unfollowed
        message = generate_message(number_of_new_followers, context, -1)
        notify(message)
        return -1

# handle user's repo updates
def handle_repo(user_repos, repo):
    #user_data = data[user.login]
    #for i in user.get_repos():
        name = repo.name
        for i_repo in user_repos:
            if i_repo["name"] == name:
                user_repo = i_repo
                break
        
        else:
            user_repo = {
                        "name": name,
                        "forks": 0,
                        "stars": 0,
                        "watchers": 0
                        }

        previous_forks = user_repo["forks"]
        previous_stars = user_repo["stars"]
        previous_watchers = user_repo["watchers"]
       
        user_repo["forks"] = current_forks = repo.forks_count
        user_repo["stars"] = current_stars = repo.stargazers_count
        user_repo["watchers"] = current_watchers = repo.watchers_count

        logic(current_stars, previous_stars, context=("starr", name)) # past tense
        
        logic(current_watchers, previous_watchers, context=("watch", name))
        
        logic(current_forks, previous_forks, context=("fork", name))
        
        for i_repo in user_data["repos"]:
            if i_repo["name"] == name:
                i_repo = user_repo
                break

        return user_data
