from helper import get_forks, get_watchers, get_stars, get_owner_name

class Repo(object):

    def __init__(self, name, owner, forks, watchers, stars, url):
        """ Represents a repository object returned by GitHub API v3.

        Parameters
        ==========
        name: str
            Name of the repository

        owner: User
            Owner of the repository

        forks: int
            Forks count of the repository

        watchers: int
            Watchers count of the repository

        stars: int
            Stars count of the repository

        url: str
            API URL of the repository

        """
        self.name = name
        self.owner = owner
        self.forks = forks
        self.watchers = watchers
        self.stars = stars
        self.url = url

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.name, self.owner,
                               self.forks, self.watchers, self.stars)

    @classmethod
    def from_name(cls, name):
        owner_name = get_owner_name(name)
        owner = User(owner_name)
        forks = get_forks(owner)
        watchers = get_watchers(owner)
        stars = get_stars(owner)
        return cls(name, owner, forks, watchers, stars)
