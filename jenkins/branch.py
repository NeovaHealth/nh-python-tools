# coding=utf-8
import urllib2
import json
import sys
import re

from optparse import OptionParser


class RepoPush(object):

    def __init__(self, json_payload):
        self._payload = json.loads(json_payload)

    @property
    def name(self):
        return self._payload['repository']['name']

    @property
    def branch(self):
        return self._payload['ref'].split('/')[-1]

    def choose_branch(self):
        """Returns branch to build against on other repositories"""
        if self.branch == 'develop' or self.branch == 'master':
            return self.branch

        if not re.match('[hf][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return 'master'

        if re.match('[h]', self.branch):
            return 'master'
        else:
            return self.branch


def get_repos(repository):
    """Returns a dict of all repos and branches."""
    repos = ['nhclinical', 'openeobs', 'nh-mobile']
    repos.remove(repository.name)
    result = {repository.name: repository.branch}

    for repo in repos:

        if is_branch(repository.choose_branch(), repo):
            result.update({repo: repository.choose_branch()})
        elif is_branch('develop', repo):
            result.update({repo: 'develop'})
        else:
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


def print_repos(repos):
    """Prints repo for the Jenkins workspace properties file."""
    print "OE_BRANCH={r[openeobs]}\nNHC_BRANCH={r[nhclinical]}" \
          "\nNHM_BRANCH={r[nh-mobile]}".format(r=repos)


parser = OptionParser()
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub push event payload')


def main():
    (options, args) = parser.parse_args()
    repo = RepoPush(options.payload)
    repos = get_repos(repo)
    print_repos(repos)


if __name__ == '__main__':
    sys.exit(main())

