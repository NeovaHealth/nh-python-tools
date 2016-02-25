# coding=utf-8
import json
import re
import urllib2

from string import punctuation
from collections import namedtuple


class PushEvent(object):

    def __init__(self, json_payload):
        self._payload = json.loads(json_payload)

    @property
    def name(self):
        return self._payload['repository']['name']

    @property
    def branch(self):
        return self._payload['ref'].split('/')[-1]

    @property
    def commit(self):
        return self._payload['head_commit']['id']

    @property
    def message(self):
        return self._payload['head_commit']['message']

    @property
    def committer(self):
        return self._payload['head_commit']['committer']['username']

    @property
    def url(self):
        return self._payload['head_commit']['url']

    @property
    def type(self):
        if self.is_feature():
            return "feature"
        elif self.is_hotfix():
            return "hotfix"
        elif self.is_master():
            return "master"
        elif self.is_develop():
            return "develop"
        else:
            return "None"

    @property
    def environment_variables(self):
        variables = ""
        variables += "GIT_HASH=" + self.commit + "\n"
        variables += "GIT_MESSAGE=" + self.message + "\n"
        variables += "GIT_AUTHOR=" + self.committer + "\n"
        variables += "GIT_URL=" + self.url + "\n"
        variables += "GIT_REPO=" + self.name + "\n"
        variables += "GIT_BRANCH=" + self.branch + "\n"
        variables += "GIT_TYPE=" + self.type + "\n"
        return variables

    def is_hotfix(self):
        if re.match('[h][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False

    def is_feature(self):
        if re.match('[f][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False

    def is_master(self):
        if self.branch == 'master':
            return True

        return False

    def is_develop(self):
        if self.branch == 'develop':
            return True

        return False


Repository = namedtuple('Repository', 'name branch')


class RepositoryNew(object):

    def __init__(self, name, branch):
        self.name = name
        self.branch = branch

    @classmethod
    def create_repository_from_push_event(cls, push):
        return cls(push.name, push.branch)

    @property
    def environment_variable(self):
        return self.name.translate(None, punctuation).upper() + "_BRANCH"


class PropertiesBuilder(object):

    def __init__(self, pushed_repository, repositories, token):
        self._token = token
        self._pushed_repository = pushed_repository
        self._build_repositories = repositories
        self.repositories = []
        self.get_repositories()

    def _get_repository(self, repository):
        """Gets required branch based on branch of pushed repository."""
        repository_branch = 'master'
        if self.is_branch(self._pushed_repository.branch, repository):
            repository_branch = self._pushed_repository.branch
        else:
            if self._pushed_repository.is_feature():
                if self.is_branch('develop', repository):
                    repository_branch = 'develop'

        self.repositories.append(Repository(repository, repository_branch))

    def get_repositories(self):
        """Gets repositories and their branches for a build."""
        self.repositories.append(
            Repository(
                self._pushed_repository.name, self._pushed_repository.branch))

        self._build_repositories.remove(self._pushed_repository.name)
        for repository in self._build_repositories:
            self._get_repository(repository)

    def is_branch(self, branch_name, repository):
        """Checks if repository has a given remote branch."""
        url = "https://api.github.com/repos/NeovaHealth/" + repository + \
              "/branches/" + branch_name

        request = urllib2.Request(url)
        request.add_header(
            'Authorization', 'token ' + self._token)

        try:
            print urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            result = False
        else:
            result = True
        return result
