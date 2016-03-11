# coding=utf-8
from unittest import TestCase

from jenkins.github import PullRequest


class TestPullRequest(TestCase):

    def setUp(self):
        payload = {
            'action': 'test_action', 'repository': {'name': 'test_name'},
            'pull_request': {'head': {'ref': 'test_branch'},
                             'merge_commit_sha': '1234', 'title': 'test',
                             'url': 'test_url',
                             'user': {'login': 'test_user'}},
            'sender': {'login': 'test_sender'}
        }
        self.pull_request = PullRequest(payload)

    def test_PullRequest_action_returns_action(self):
        self.assertEqual(self.pull_request.action, 'test_action')

    def test_PullRequest_name_returns_repo_name(self):
        self.assertEqual(self.pull_request.name, 'test_name')

    def test_PullRequest_branch_returns_branch_name(self):
        self.assertEqual(self.pull_request.branch, 'test_branch')

    def test_PullRequest_commit_returns_commit_hash(self):
        self.assertEqual(self.pull_request.commit, '1234')

    def test_PullRequest_message_returns_pull_request_message(self):
        self.assertEqual(self.pull_request.message, 'test')

    def test_PullRequest_pusher_returns_login_user_who_pushed(self):
        self.assertEqual(self.pull_request.pusher, 'test_user')

    def test_PullRequest_committer_returns_of_login_of_last_committer(self):
        self.assertEqual(self.pull_request.committer, 'test_sender')

    def test_PullRequest_url_returns_url_of_pull_request(self):
        self.assertEqual(self.pull_request.url, 'test_url')

    def test_environment_variables_returns_string(self):
        variables = 'GIT_HASH=1234\nGIT_MESSAGE="test"\n' \
                    'GIT_AUTHOR=test_sender\nGIT_PUSHER=test_user\n' \
                    'GIT_URL=test_url\nPUSHED_REPO=test_name\n' \
                    'PUSHED_BRANCH=test_branch\nGIT_TYPE=None\nUAT_ON=true\n' \
                    'PIPELINE_RUN=0\n'

        self.assertEqual(self.pull_request.environment_variables, variables)

