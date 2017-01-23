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
        user = self.get_blob(handle)
        followers = user['followers']
        repos = self.get_repos(handle)
        return cls(username, followers, repos)

    def get_blob(self, handle):
        if handle == USERNAME:
            user_url = URL + '/user'

        else:
            user_url = URL + '/users/' + handle

        user = requests.get(user_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
        return user

    def get_repos(self, handle):
        if self.username == USERNAME:
            repo_url = URL + '/user/repos'

        else:
            repo_url = URL + '/users/' + handle + '/repos'
        
        repo_response = requests.get(repo_url, headers=HEADERS, auth=(USERNAME, PASSWORD)).json()
        repos = [Repo.from_name(repo[name], repo[owner][login]) for repo in repo_response]
        return repos

    def get_notifications(self):
        # changes in followers
        # notification
        old_count # from DB
        new_count = self.followers

        if old_count == new_count:
            return None

        else:
            if self.username == USERNAME:
                notification_url = URL + '/user/followers'
                target = 'you'

            else:
                notification_url = URL + '/users/' + self.username + '/followers'
                target = self.username

            notifications = []
            if new_count > old_count:
                params = {'per_page': self.followers}
                start_page = old_count // 100
                end_page = new_count // 100
                followers = []
                for i in range(start_page, end_page + 1):
                    params['page'] = i
                    followers.append(requests.get(notification_url, headers = HEADERS,
                                                  params = params, auth=(USERNAME, PASSWORD)))

                start_index = old_count % 100
                context = "follow"
                for user_blob in followers[start_index:]:
                    protagonist = user_blob['login']
                    notifications.append(Notification.generate_message(target, protagonist, context))

            else:
                message = '{} users unfollowed {}'.format(old_count - new_count, target)
                notifications.append(Notification(message))

        return notifications
