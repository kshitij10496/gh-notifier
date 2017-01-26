import json
import requests

from notification import Notification
from repo import Repo
from settings import USER_DATA, USERNAME, PASSWORD, URL, HEADERS

class User(object):
    """ Represents a user encapsulating the GitHub User object. """

    def __init__(self, username, followers=0, repos=None):
        """ Initialises a User object.

          Parameters
        ==========
        username: str
            GitHub username/handle of the user

        followers: int
            No. of GitHub followers of the user

        repos: list
            List of all the user's repositories on GitHub.
            This includes repositories owned by the authenticated user, repositories
            where the user is a collaborator, and repositories that the user has
            access to through an organization membership.

        """
        self.username = username
        self.followers = followers
        self.repos = repos

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__, self.username,
                                       self.followers, self.repos)

    @classmethod
    def from_handle(cls, handle):
        """ Alternate constructor for instantiating an User by its handle.

        Parameters
        ==========
        handle: str
            User's GitHub username/handle.

        """
        username = handle
        user = get_blob(handle)
        followers = user['followers']
        repos = get_repos(handle)
        return cls(username, followers, repos)

    def get_notifications(self, old_count):
        # changes in followers
        # notification
        new_count = self.followers
        notifications = []

        if old_count != new_count:
            if self.username == USERNAME:
                notification_url = URL + '/user/followers'
                target = 'you'

            else:
                notification_url = URL + '/users/' + self.username + '/followers'
                target = self.username

            if new_count > old_count:
                params = {'per_page': self.followers}
                start_page = old_count // 100
                end_page = new_count // 100
                followers = []
                with requests.Session() as s:
                    for i in range(start_page + 1, end_page + 2):
                        params['page'] = i
                        new_page = s.get(notification_url, headers=HEADERS,
                                         params=params, auth=(USERNAME, PASSWORD)).json()
                        print("Length of page {} : {}".format(i, len(new_page)))
                        followers += new_page

                start_index = old_count % 100
                context = "follow"
                print("Len of followers:" + str(len(followers)))
                print("Len of list:" + str(len(followers[start_index:])))
                for user_blob in followers[start_index:]:
                    protagonist = user_blob['login']
                    notifications += [Notification.generate_message(protagonist, context, target)]

            else:
                message = '{} users unfollowed {}'.format(old_count - new_count, target)
                notifications += [Notification(message)]

        return notifications

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def get_blob(handle):
    if handle == USERNAME:
        user_url = URL + '/user'

    else:
        user_url = URL + '/users/' + handle

    print("User = " + USERNAME + " : " + user_url)
    user = requests.get(user_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
    return user

def get_repos(handle):
    if handle == USERNAME:
        repo_url = URL + '/user/repos'

    else:
        repo_url = URL + '/users/' + handle + '/repos'

    repo_response = requests.get(repo_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
    repos = [Repo.from_Repository(repo) for repo in repo_response]
    return repos
