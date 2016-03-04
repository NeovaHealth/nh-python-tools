# coding=utf-8
from event import Event


def github_event_factory(payload):
    if 'pull_request' in payload:
        return PullRequest(payload)
    else:
        return Push(payload)


class PullRequest(Event):

    def __init__(self, payload):
        self._payload = payload

    @property
    def action(self):
        return self._payload['action']

    @property
    def name(self):
        return self._payload['repository']['name']

    @property
    def branch(self):
        return self._payload['pull_request']['head']['ref']

    @property
    def commit(self):
        return self._payload['pull_request']['merge_commit_sha']

    @property
    def message(self):
        return self._payload['pull_request']['title']

    @property
    def pusher(self):
        return self._payload['pull_request']['user']['login']

    @property
    def committer(self):
        return self._payload['sender']['login']

    @property
    def url(self):
        return self._payload['pull_request']['url']

    @property
    def environment_variables(self):
        variables = ""
        variables += "GIT_HASH=" + self.commit + "\n"
        variables += "GIT_MESSAGE=" + '\"' + self.message + '\"' + "\n"
        variables += "GIT_AUTHOR=" + self.committer + "\n"
        variables += "GIT_PUSHER=" + self.pusher + "\n"
        variables += "GIT_URL=" + self.url + "\n"
        variables += "PUSHED_REPO=" + self.name + "\n"
        variables += "PUSHED_BRANCH=" + self.branch + "\n"
        variables += "GIT_TYPE=" + self.type + "\n"
        variables += "UAT_ON=true\n"
        if self.action not in ["opened", "reopened"]:
            variables += "PIPELINE_RUN=0\n"
        else:
            variables += "PIPELINE_RUN=1\n"
        return variables


class Push(Event):

    def __init__(self, payload):
        self._payload = payload

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
    def pusher(self):
        return self._payload['pusher']['name']

    @property
    def committer(self):
        return self._payload['head_commit']['committer']['username']

    @property
    def url(self):
        return self._payload['head_commit']['url']

    @property
    def environment_variables(self):
        variables = ""
        variables += "GIT_HASH=" + self.commit + "\n"
        variables += "GIT_MESSAGE=" + '\"' + self.message + '\"' + "\n"
        variables += "GIT_AUTHOR=" + self.committer + "\n"
        variables += "GIT_PUSHER=" + self.pusher + "\n"
        variables += "GIT_URL=" + self.url + "\n"
        variables += "PUSHED_REPO=" + self.name + "\n"
        variables += "PUSHED_BRANCH=" + self.branch + "\n"
        variables += "GIT_TYPE=" + self.type + "\n"
        variables += "UAT_ON=false\n"
        variables += "PIPELINE_RUN=1\n"
        return variables
