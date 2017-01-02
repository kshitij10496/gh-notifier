from __future__ import division
import sys
from math import ceil
import requests

base_url = 'https://api.github.com/search/users'


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


def search_location(location, keyword=None, max_users=10, params={}):
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
    params['per_page'] = 100
    if keyword is not None:
        new_params = user_search_filter(keyword)
        params.update(new_params)

    response = requests.get(base_url, params=params)
    content = response.json()
    total_users = content['total_count']
    number_of_users = min(max_users, total_users)
    number_of_pages = int(number_of_users / 100)
    
    users = _get_users(response.json()['items'])
    for i in range(2, number_of_pages):
        params['page'] = i
        r = requests.get(base_url, params=params)
        new_users = _get_users(r.json()['items'])
        users.append(new_users)
    
    return users[:number_of_users]


def _get_users(user_list):
    users = []
    for user in user_list:
        users.append(user["login"])

    return users
