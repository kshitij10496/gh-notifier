import requests
from bs4 import BeautifulSoup


def user_kitchen(handle):
    """Function to make soup for a user.

    Parameters
    ==========

    handle : str
        The GitHub handle of the user

    Returns
    =======

    soup : BeautifulSoup
    """
    base_url = 'https://github.com/'
    user = base_url + handle
    r = requests.get(user)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    return soup


def detail_scrapper(soup, attribute):
    """Function to scrape user and profile details from the soup."""
    tagset = soup.find_all(attrs=attribute)
    data = []
    for tag in tagset:
        data.append(tag.text)

    return data


class User(object):
    """The class to represent a GitHub user.

    Each user is identified by his unique GitHub handle.
    """
    details_map = {'fullname': {'class': 'vcard-fullname'},
                   'bio': {'class': 'user-profile-bio'},
                   'company': {'aria-label': 'Organization'},
                   'location': {'aria-label': 'Home location'},
                   'email': {'aria-label': 'Email'},
                   'membership': {'aria-label': 'Member since'}}

    def __init__(self, handle):
        self.handle = str(handle)
        self.soup = user_kitchen(handle)
        self.user_details()
        self.profile_details()

    def user_details(self):
        value_map = {}
        for detail, attribute in details_map.items():
            value_map[detail] = detail_scrapper(self.soup, attribute)[0]

        self.fullname = value_map['fullname']
        self.bio = value_map['bio']
        self.company = value_map['company']
        self.location = value_map['location']
        self.email = value_map['email']
        self.membership = value_map['membership']

    def profile_details(self):
        attribute = {'class': 'vcard-stat-count d-block'}
        self.followers, self.starred, self.following = detail_scrapper(self.soup, attribute)
        self.organizations = _get_organizations()

    def _get_organizations(self):
        bar = self.soup.find_all(attrs={'class': 'clearfix'})[0].find_all('a')
        organizations = []
        for i in bar:
            org = i.get('aria-label')
            organizations.append(org)
        return organizations

    def profile_pic(self):
        link = self.soup.find_all('img', class_='avatar rounded-2')[0].get('src')
        return link
