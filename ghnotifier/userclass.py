class User(object):

    def __init__(self, username, followers, repos, notifications):
        """ Represents a user encapsulating the GitHub User object.

          Parameters
        ==========
        username: str
            GitHub username/handle of the user

        followers: int
            No. of GitHub followers of the user

        repos: list
            List of all the user's repositories on GitHub

        notifications: list
            List of the user's GitHub notifications

        """
        self.username = username
        self.followers = followers
        self.repos = repos
        self.notifications = notifications
        
    def __repr__():
        return "{}({})".format(self.__class__.__name__, self.username)

    @classmethod
    def from_handle(cls, handle):
        username = handle
        followers = get_followers(handle)
        repos = get_repos(handle)
        notifications = get_notifications(handle)
        return cls(username, followers, repos, notifications)
