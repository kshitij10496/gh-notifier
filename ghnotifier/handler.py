import os
import json
import getpass

from github import Github

from .notifier import notify, generate_message

USER_CREDENTIALS = os.path.expanduser('~') + '/.ghnotifier_config'
USER_DATA = os.path.expanduser('~') + '/.ghnotifier_data'

def create_user():

    # read/create a configuration file for user credentials
    try:
        with open(USER_CREDENTIALS, 'r') as f:
            credentials = json.load(f)

    except FileNotFoundError:
        with open(USER_CREDENTIALS, 'w') as f:
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
        with open(USER_DATA, 'r') as fp:
            pass

    except FileNotFoundError:
        with open(USER_DATA, 'w') as fp:
            # Schema for user data
            data = {
                    credentials["USERNAME"]:
                        {
                            "followers": 0,
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
    with open(USER_DATA, 'r') as fp:
        user_data = json.load(fp)[user.login]

    followers_status = handle_followers(user_data["followers"], user)
    user_data["followers"] = user.followers
    print("Execution of handle_followers is over.")
    print("Execution of handling repos is commencing.")
    for repo in user.get_repos():
        print("Handling repo: %s", repo.name)
        for i, old_repo in enumerate(user_data["repos"]):
            if repo.name in old_repo:
                updated_repo = handle_repo(old_repo, repo)
                user_data["repos"][i] = updated_repo
                break           
        else:
            new_repo = {
                        "name": repo.name,
                        "forks": 0,
                        "stars": 0,
                        "watchers": 0
                        }
        
            updated_repo = handle_repo(new_repo, repo)
            user_data["repos"].append(updated_repo) 
        print("Handling %s over", repo.name)

    print("Writing data")
    with open(USER_DATA, 'w') as fp:
        json.dump(user_data, fp)


def logic(current_data, previous_data, context=None):
    delta = current_data - previous_data
    if delta == 0:
        return 0

    elif delta > 0:
        message = generate_message(delta, context, 1)

    else:
        message = generate_message(delta, context, -1)

    notify(message)
    return 1

# handle user's followers updates
def handle_followers(user_followers, user):
    previous_followers = user_followers
    user_followers = current_followers = user.followers
    context = ("follow", user.login)

    followers_handle = []
    number_of_new_followers = current_followers - previous_followers
    if(number_of_new_followers == 0): # no change in following
        return 0

    elif(number_of_new_followers > 0): # new followers
        for follower in user.get_followers()[previous_followers:]:
            followers_handle.append(follower.login)

        for f in followers_handle:
            message = generate_message(f, context, 1)
            notify(message)

        return 1

    else: # people unfollowed
        message = generate_message(number_of_new_followers, context, -1)
        notify(message)
        return -1

# handle user's repo updates
def handle_repo(user_repo, repo):
        previous_forks = user_repo["forks"]
        previous_stars = user_repo["stars"]
        previous_watchers = user_repo["watchers"]
       
        user_repo["forks"] = current_forks = repo.forks_count
        user_repo["stars"] = current_stars = repo.stargazers_count
        user_repo["watchers"] = current_watchers = repo.watchers_count

        name = repo.name
        logic(current_stars, previous_stars, context=("starr", name)) # past tense
        logic(current_watchers, previous_watchers, context=("watch", name))
        logic(current_forks, previous_forks, context=("fork", name))

        return user_repo
