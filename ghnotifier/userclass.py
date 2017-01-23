class User(object):

    def __init__(self, username, followers, repos):
        """ Represents a user encapsulating the GitHub User object.

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
 
    def __repr__():
        return "{}({})".format(self.__class__.__name__, self.username)

    @classmethod
    def from_handle(cls, handle):
        username = handle

        if handle == USERNAME:
            user_url = URL + '/user'
            repo_url = URL + '/user/repos'

        else:
            user_url = URL + '/users/' + handle
            repo_url = URL + '/users/' + handle + '/repos'

        user = requests.get(user_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
        followers = user['followers']
        
        repo_response = requests.get(repo_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
        repos = [Repo.from_name(repo[name], repo[owner][login]) for repo in repo_response]

        return cls(username, followers, repos)

    def get_notifications():
        pass
