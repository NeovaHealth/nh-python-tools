# coding=utf-8
from event import Event


class TravisEvent(Event):

    def __init__(self, payload):
        self._payload = payload
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
    def trigger_type(self):
        if self.is_pull_request():
            return "TRIGGER_TYPE=" + "github-pull-request"
        else:
            return "TRIGGER_TYPE=" + "git-commit"

    @property
    def environment_variables(self):
        result = ""
        if self.is_pull_request():
            result += self.pull_request_id + '\n'

        result += self.git_hash + '\n' + self.git_repo + '\n' + \
                  self.pushed_branch + '\n' + self.git_type + '\n' + \
                  self.uat + '\n' + self.trigger_type + '\n'
        return result

    def is_pull_request(self):
        if self.pull_request != 'false':
            return True

        return False
