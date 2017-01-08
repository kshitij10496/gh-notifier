from github import Github
from settings import USERNAME, PASSWORD

g = Github(USERNAME, PASSWORD)

user = g.get_user()

# create a data storage file

def logic(current_data, previous_data, context=None):
    number_of_new_followers = current_data -  previous_data
    if( previous_data == 0): # no change in following
        return 0

    elif( previous_data > 0): # new followers
        # update DB
        for follower in user.get_followers[previous_data:]:
            notify("{} started {}ing you".format(follower.name, *context))
        
        return 1

    else: # people unfollowed
        # update DB
        notify("{} users un{}ed {}".format(number_of_new_followers, *context))
        return -1

# handle user's followers updates
def user_followers(user):
    current_followers = user.followers
    return logic(current_followers, previous_followers, context=("follow", "you"))

# handle user's repo updates
#
# for i in user.get_repos():
#    name = i.name
#    forks = i.forks_count
#    stars = i.stargazers_count
#    watchers = i.watchers_count
#    logic()

