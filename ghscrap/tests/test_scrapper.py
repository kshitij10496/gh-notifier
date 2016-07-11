import pytest

from ghscrap.scrapper import user_search_filter, search_location


def test_user_search_filter():
    filterkeys = ['most followed', 'least followed', 'most repos',
                  'fewest repos', 'recently joined', 'oldest to join GitHub']

    filters = [
               {'s': 'followers', 'o': 'desc'}, {'s': 'followers', 'o': 'asc'},
               {'s': 'repositories', 'o': 'desc'}, {'s': 'repositories', 'o': 'asc'},
               {'s': 'joined', 'o': 'desc'}, {'s': 'joined', 'o': 'asc'}
              ]

    for i in range(len(filters)):
        assert user_search_filter(filterkeys[i]) == filters[i]

    with pytest.raises(ValueError):
        user_search_filter("oldest here")


def test_search_location():
    location = 'Kharagpur'
    handles = ['hargup', 'OrkoHunter', 'vivekiitkgp', 'amrav', 'kshitij10496']

    assert search_location(location, max_users=5) == handles
    assert search_location(location, "most followed", max_users=5) == handles
