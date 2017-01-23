from helper import get_forks, get_watchers, get_stars, get_owner_name

class Repo(object):

    def __init__(self, name, owner, forks, watchers, stars):
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
        self.url = 'https://github.com/' + owner + '/' + name

    def __repr__(self):
        return '{}({}, {}, {}, {}, {})'.format(self.__class__.__name__,
                                               self.name, self.owner, self.forks,
                                               self.watchers, self.stars)

    @classmethod
    def from_name(cls, repo_name, owner_name):
        url = URL + '/repos/' + owner_name + repo_name
        repo = requests.get(url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
        # handle pagination

        #owner = owner_name
        #name = repo_name
        #forks = repo['forks_count']
        #watchers = repo['watchers_count']
        #stars = repo['stargazers_count']
        #return cls(name, owner, forks, watchers, stars)
        return cls.from_Repository(repo)

    @classmethod
    def from_Repository(repo):
        name = repo['name']
        owner = User(repo['owner']['login'])
        forks = repo['forks_count']
        watchers = repo['watchers_count']
        stars = repo['stargazers_count']
        return cls(name, owner, forks, watchers, stars)

    def get_notifications():
        pass
