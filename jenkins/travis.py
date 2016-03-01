# coding=utf-8
import json
import re


class TravisEvent(object):

    def __init__(self, payload):
        self._payload = json.loads(payload)
        self.pipeline = "PIPELINE_RUN=1"
        self.uat = "UAT_ON=false"

    @property
    def name(self):
        return self._payload['repository']['name'].split('/')[-1]

    @property
    def branch(self):
        return self._payload['branch']

    @property
    def commit(self):
        return self._payload['commit']

    @property
    def pull_request(self):
        return self._payload['pull_request']

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
    def git_hash(self):
        return "GIT_HASH=" + self.commit

    @property
    def git_repo(self):
        return "PUSHED_REPO=" + self.name

    @property
    def pushed_branch(self):
        return "PUSHED_BRANCH=" + self.branch

    @property
    def git_type(self):
        return "GIT_TYPE=" + self.type

    @property
    def pull_request_id(self):
        return "PULL_REQUEST_ID=" + self.pull_request

    @property
    def environment_variables(self):
        result = self.git_hash + '\n' + self.git_repo + '\n' + \
                  self.pushed_branch + '\n' + self.git_type + '\n' + \
                  self.pull_request_id + '\n' + self.uat + '\n'
        return result

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

