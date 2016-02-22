# coding=utf-8
import urllib2
import json


def get_repos(repo_branch):
    repos = ['nhclinical', 'openeobs', 'nh-mobile']
    repos.remove(repo_branch['repository'])

    result = {repo_branch['repository']: repo_branch['branch']}
    for repo in repos:
        if repo_branch['branch'].startswith('f'):
            if is_branch(repo_branch['branch'], repo):
                result.update({repo: repo_branch['branch']})
            elif is_branch('develop', repo):
                result.update({repo: 'develop'})
            else:
                result.update({repo: 'master'})

        if repo_branch['branch'].startswith('h'):
            if is_branch(repo_branch['branch'], repo):
                result.update({repo: repo_branch['branch']})
            else:
                result.update({repo: 'master'})

        if repo_branch['branch'] == 'develop':
            if is_branch('develop', repo):
                result.update({repo: 'develop'})
            else:
                result.update({repo: 'master'})

        if repo_branch['branch'] == 'master':
            result.update({repo: 'master'})

    return result


def is_branch(branch_name, repository):
    url = "https://api.github.com/repos/NeovaHealth/" + repository + \
          "/branches/" + branch_name
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError:
        result = False
    else:
        result = True
    return result


def get_branch(json_payload):
    """
    Gets branch and repository name from GitHub
    push event payload.
    """
    data = dict(repository=None, branch=None)
    payload = json.load(json_payload)
    data['repository'] = payload['repository']['name']
    branch = payload['ref'].split('/')[-1]
    data['branch'] = branch
    return data

