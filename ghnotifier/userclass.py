class User(object):

    def __init__(self, username):
        self.username = username
        self.name = None
        self.followers
        self.repos # list of Repo objects
        self.notifications # list of Notification object

    def __repr__():
        return "{}({})".format(self.__class__.__name__, self.username)

    