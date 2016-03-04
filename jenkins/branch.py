# coding=utf-8
import urllib2
import base64

from collections import namedtuple

Repository = namedtuple('Repository', 'name branch')


class BranchPicker(object):

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
        url = "https://api.github.com/repos/neovahealth/" + repository + \
              "/branches/" + branch_name
        base64string = base64.encodestring(self._token).replace('\n', '')
        request = urllib2.Request(url)
        request.add_header("Authorization", "Basic %s" % base64string)

        try:
            urllib2.urlopen(request)
        except urllib2.HTTPError:
            result = False
        else:
            result = True
        return result
