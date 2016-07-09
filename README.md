# gh-scrapper

[![Join the chat at https://gitter.im/kshitij10496/gh-scrapper](https://badges.gitter.im/kshitij10496/gh-scrapper.svg)](https://gitter.im/kshitij10496/gh-scrapper?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
GitHub Scrapper written in Python

This library aims to provide an extensive mechanism for scrapping resources from GitHub.  
The project is in pre-alpha stage and is under heavy developement.


#### Usage
-----------------

For instance, lets say that we are interested in users present in `"Kharagpur"`.
Our aim is to get the list of handles of top 10 users (result from "Best match" filter).

**API**

From a Python shell from the project repo:

```python

In []: from ghscrap.scrapper import search_location

In []: users = search_location("Kharagpur", max_users=10)

In []: for user in users:
  ...:     print(user)
  ...:
hargup
OrkoHunter
vivekiitkgp
amrav
kshitij10496
sam17
icyflame
hjpotter92
shivamvats
ankeshanand

```

**Commandline Interface**

```
$ python main.py location filename max-users
```
`location` : the location of interest  
`filename` : the text file to write the results in.  
`max-users`: the maximum number of users you are interested.
             By default, it has been set to 50.

For our test case, we can run our script as:

```
$ python main.py Kharagpur kgp.txt 10
```

Viola ! We have our text file `kgp.txt` that has the same list of names as above.

### Features

Currently supported:

- [x] Search for users based on their location

**TODOs**:

- [ ] Specified user's details
- [ ] Contribution details
- [ ] Add options for filtering search


### Contributing

Please feel free to report all the issues and/or feature requests.
I will try to work on them.  
More so, it would be great if we can collaborate.

Scrape GitHub Away !

