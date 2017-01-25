import requests

from settings import URL, HEADERS, USERNAME, PASSWORD
from notification import Notification

class Repo(object):

    def __init__(self, name, owner, forks, watchers, stars):
        """ Represents a repository object returned by GitHub API v3.

        Parameters
        ==========
        name: str
            Name of the repository

        owner: str
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
        url = URL + '/repos/' + owner_name + "/" + repo_name
        print("Repo = " + repo_name + ' : ' + url)
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
    def from_Repository(cls, repo):
        name = repo['name']
        owner = repo['owner']['login']
        forks = repo['forks_count']
        watchers = repo['watchers_count']
        stars = repo['stargazers_count']
        return cls(name, owner, forks, watchers, stars)

    def get_notifications(self, old_stars, old_watchers, old_forks):
        new_stars, new_watchers, new_forks = self.stars, self.watchers, self.forks

        delta_stars = new_stars - old_stars
        delta_watchers = new_watchers - old_watchers
        delta_forks = new_forks - old_forks

        notifications = []
        if delta_stars != 0:
            context = 'starr'
            if delta_stars < 0:
                context = 'un' + context # not a typo

            notifications.append(Notification.generate_message('{} users'.format(delta_stars), context, self.name))

        if delta_watchers != 0:
            context = 'watch'
            if delta_watchers < 0:
                context = 'un' + context

            notifications.append(Notification.generate_message('{} users'.format(delta_watchers), context, self.name))

        if delta_forks != 0:
            context = 'fork'
            if delta_forks < 0:
                context = 'un' + context

            notifications.append(Notification.generate_message('{} users'.format(delta_watchers), context, self.name))

        return notifications
