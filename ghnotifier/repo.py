class Repo(object):

    def __init__(self, name):
        self._name = name
        self._forks = None

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self._name)

    @property
    def forks(self):
        self._forks = 10

    @property
    def owner(self):

    @property
    def watchers(self):

    @property
    def stargazers(self):
