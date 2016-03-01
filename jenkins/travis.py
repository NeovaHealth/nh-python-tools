# coding=utf-8
import json
import re


class TravisEvent(object):

    def __init__(self, payload):
        self._payload = json.loads(payload)

    @property
    def name(self):
        return self._payload['repository']['name']

    @property
    def branch(self):
        return self._payload['branch']

    @property
    def commit(self):
        return self._payload['commit']

    @property
    def message(self):
        return self._payload['message']

    @property
    def committer(self):
        return self._payload['committer_name']

    @property
    def event_type(self):
        return self._payload['type']

    @property
    def url(self):
        return self._payload['repository']['url']

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
        variables += "GIT_PUSHER=" + self.committer + "\n"
        variables += "GIT_URL=" + self.url + "\n"
        variables += "PUSHED_REPO=" + self.name + "\n"
        variables += "PUSHED_BRANCH=" + self.branch + "\n"
        variables += "GIT_TYPE=" + self.type + "\n"
        variables += "UAT_ON=false\n"
        variables += "PIPELINE_RUN=1\n"
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


