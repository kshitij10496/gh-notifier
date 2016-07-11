from __future__ import division
import sys
from math import ceil
import requests
from bs4 import BeautifulSoup

base_url = 'https://github.com/search/'


def kitchen(params):
    """Returns a BeautifulSoup prepared in the kitchen."""
    r = requests.get(base_url, params=params)
    data = r.text
    soup = BeautifulSoup(data, 'lxml')
    return soup


def user_search_filter(filterkey):
    """Filter for user search pages.

    Parameters
    ==========

    filterkey : String
        The keyword to filter the results out based on some criteria.

        Currently, the following criterias are supported:
        1. Number of followers := 'Most followers' or 'Fewest followers'
        2. Number of repositories := 'Most repositories' or 'Fewest repositories'
        3. Relative date of joining := 'Most recently joined' or 'Least recently joined'
        If nothing is passed, the result of 'Best Match' is returned.

    Returns
    =======

    dict
        A dictionary of search parameters based on `filterkey`.

    """
    user_search_parameters = ('follow', 'repo', 'join')
    measure_table = {'desc': ('most', 'high', 'large'), 'asc': ('least', 'less', 'few')}
    timeline_table = {'desc': ('recent', 'new'), 'asc': ('last', 'old')}

    search_params = {}

    if any(parameter in filterkey for parameter in user_search_parameters):
        if 'join' in filterkey:
            search_params['s'] = 'joined'
            table = timeline_table

        else:
            table = measure_table
            if 'follow' in filterkey:
                search_params['s'] = 'followers'
            else:
                search_params['s'] = 'repositories'

        if any(word in filterkey for word in table['asc']):
            search_params['o'] = 'asc'

        else:
            search_params['o'] = 'desc'  # the default behaviour returns "Most followers".

    else:
        raise ValueError("Enter a valid filterkey. Read the documentation "
                         "to know about the supported search parameters.")

    return search_params


def search_location(location, keyword=None, max_users=50, params={}):
    """Location based search.

    Parameters
    ==========

    location : String
        The name of the concerned location.

    keyword : String
        The filter for search a criteria.

    max_users : int
        The maximum number of users of interest.
        Using a number larger than 100 can lead to loss of results due to
        making "Too Many Requests" [HTTP Status Code: 429].

    params : dict
        Any specified parameters.

    Returns
    =======

    list
        A list of handles of the users at a particular location based on the
        specified criterias(if any).

    """
    params['q'] = 'location:' + location
    if keyword is not None:
        new_params = user_search_filter(keyword)
        params.update(new_params)

    soup = kitchen(params)
    return _search_location(soup, max_users, params)


def _search_location(soup, max_users, params):
    """Helper to search_location."""
    number_of_users = int(soup.find_all('h3')[1].text.split()[2])
    max_pages = ceil(max_users / 10) + 1
    search_pages = ceil(number_of_users / 10) + 1
    number_of_pages = int(min(max_pages, search_pages))

    users = []
    for i in range(1, number_of_pages):
        users.extend(search_page_users(i, params=params))

    if len(users) > max_users:
        users = users[:max_users]

    return users


def search_page_users(p, params={}):
    """Returns a list of handles on a search result page."""
    params['p'] = str(p)
    soup = kitchen(params)
    return _search_page_users(soup, params)


def _search_page_users(soup, params):
    """Helper to search_page_users."""
    users = []
    user_list = soup.find_all('div', class_="user-list-info")
    for user in user_list:
        users.append(user.find('a').text)

    return users


def main():
    location = str(sys.argv[1])
    filename = str(sys.argv[2])

    if len(sys.argv) > 3:
        max_users = int(sys.argv[3])
        users = search_location(location, max_users=max_users)
    else:
        users = search_location(location)

    f = open(filename, 'w')
    for user in users:
        f.write(user + '\n')

    f.close()


if __name__ == '__main__':
    main()
