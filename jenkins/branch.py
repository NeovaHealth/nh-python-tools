# coding=utf-8
import urllib2
import json
import sys

from optparse import OptionParser

from regex import regex_method


def get_repos(repo_branch):
    """Returns a dict of all repos and branches."""
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
    payload = json.loads(json_payload)
    data['repository'] = payload['repository']['name']

    if not regex_method(payload['ref']):
        raise Exception("Branch name is incorrect format: %s" % payload['ref'])

    branch = payload['ref'].split('/')[-1]
    data['branch'] = branch
    return data


parser = OptionParser()
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub push event payload')


def main():
    print "Starting search ...\n"
    (options, args) = parser.parse_args()
    pushed = get_branch(options.payload)
    repos = get_repos(pushed)
    print repos
    print "\nFinished!"


if __name__ == '__main__':
    sys.exit(main())

