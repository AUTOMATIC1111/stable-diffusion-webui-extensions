#!/usr/bin/env python3

# Update the github stars
# 1. Get the list of extensions from the json file
# 2. Get the github stars for each extension
# 3. Update the json file with the github stars

import json
import requests
import regex as re

def get_github_stars(extension_url):
    """
    Get the github stars for the extension
    using the http://api.github.com/repos/[username]/[reponame] {stargazers_count}
    Unauthenticated requests are limited to 60 per hour.
    extension_url: https://github.com/[username]/[reponame](.git)?
    return: number of stars
    """
    github_url = extension_url.replace('github.com', 'api.github.com/repos')
    # remove the .git from the url (ONLY IN THE END)
    github_url = re.sub(r'\.git$', '', github_url)
    
    # Authenticate to get 5000 requests per hour
    Token = '' # Add your github token here
    headers = {}
    if Token:
        headers = {'Authorization': 'token ' + Token}
    try:
        r = requests.get(github_url, headers=headers)
        if r.status_code == 200:
            return r.json()['stargazers_count']
        else:
            print("Tried to get the stars for: ", github_url)
            print('Error: ', r.status_code)
            return 0
    except Exception as e:
        print("Tried to get the stars for: ", github_url)
        print('Error: ', e)
        return 0

def update_github_stars():
    """
    Get the list of extensions from the index.json file
    Get the github stars for each extension
    Update the json file with the github stars
    """
    with open('index.json') as json_file:
        data = json.load(json_file)
        for extension in data['extensions']:
            print(extension['name'])
            stars = get_github_stars(extension['url'])
            if stars > 0:
                extension['stars'] = stars
    with open('index.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    update_github_stars()