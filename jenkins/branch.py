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

    def is_hotfix(self):
        if re.match('[h][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False

    def is_feature(self):
        if re.match('[f][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False


def get_repositories(pushed_repository):
    """Gets repositories and their branches for a build."""
    repositories = ['nhclinical', 'openeobs', 'nh-mobile']
    repositories.remove(pushed_repository.name)
    result = {pushed_repository.name: pushed_repository.branch}

    for repository in repositories:
        result.update(get_repository(pushed_repository, repository))

    return result


def get_repository(pushed_repository, other_repository):
    """Gets required branch based on branch of pushed repository."""
    result = {}

    if is_branch(pushed_repository.branch, other_repository):
        result.update({other_repository: pushed_repository.branch})
    else:
        if pushed_repository.is_hotfix():
            result.update({other_repository: 'master'})
        elif pushed_repository.is_feature():
            if is_branch('develop', other_repository):
                result.update({other_repository: 'develop'})
            else:
                result.update({other_repository: 'master'})
        else:
            result.update({other_repository: 'master'})

    return result


def is_branch(branch_name, repository):
    """Checks if repository has a given remote branch."""
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
    """
    Prints environment variables for the Jenkins workspace
    properties file.
    """
    print "OE_BRANCH={r[openeobs]}\nNHC_BRANCH={r[nhclinical]}" \
          "\nNHM_BRANCH={r[nh-mobile]}".format(r=repos)


parser = OptionParser()
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub push event payload')


def main():
    (options, args) = parser.parse_args()
    repo = RepoPush(options.payload)
    repos = get_repositories(repo)
    print_repos(repos)


if __name__ == '__main__':
    sys.exit(main())