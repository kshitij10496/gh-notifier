class Repo(object):

    def __init__(self, name, owner, forks, watchers, stars, url):
        """
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
        owner_name = get_user()
        owner = User(owner_name)
        forks = get_forks()
        watchers = get_watchers()
        stars = get_stars()
        return cls(name, owner, forks, watchers, stars)
