# coding=utf-8
import json
import re

from collections import namedtuple

from utils import is_branch


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

    def is_master(self):
        if self.branch == 'master':
            return True

        return False


Repository = namedtuple('Repository', 'name branch')


class PropertiesBuilder(object):

    def __init__(self, pushed_repository, repositories):
        self._pushed_repository = pushed_repository
        self._build_repositories = repositories
        self.repositories = []
        self.get_repositories()

    def _get_repository(self, repository):
        """Gets required branch based on branch of pushed repository."""
        repository_branch = 'master'
        if is_branch(self._pushed_repository.branch, repository):
            repository_branch = self._pushed_repository.branch
        else:
            if self._pushed_repository.is_feature():
                if is_branch('develop', repository):
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
