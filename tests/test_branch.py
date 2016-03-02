# coding=utf-8
from unittest import TestCase

from jenkins.branch import PushEvent, GithubEvent


class TestPushEvent(TestCase):

    def setUp(self):

        self.json_string = '{"ref": "refs/heads/master", "repository": ' \
                           '{"name": "public-repo"}, "head_commit": ' \
                           '{"id": "1", "message": "test_message", ' \
                           '"committer": {"username": "test_user"}, ' \
                           '"url": "http://"}, "pusher": {"name": ' \
                           '"test_pusher"}}'
        self.json_string = GithubEvent(self.json_string)._payload

        self.json_string_develop = '{"ref": "refs/heads/develop", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_develop = GithubEvent(self.json_string_develop)._payload
        self.json_string_feature = '{"ref": "refs/heads/f1234_test", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_feature = GithubEvent(self.json_string_feature)._payload
        self.json_string_hotfix = '{"ref": "refs/heads/h1234_test", ' \
                                  '"repository": {"name": "public-repo"}}'
        self.json_string_hotfix = GithubEvent(self.json_string_hotfix)._payload

    def test_PushEvent_has_instance_attributes_name_and_branch(self):
        result = PushEvent(self.json_string)

        self.assertEqual(result.name, 'public-repo')
        self.assertEqual(result.branch, 'master')

    def test_PushEvent_is_master_returns_True_when_master_branch(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.is_master(), True)

    def test_PushEvent_is_master_returns_False_when_not_master_branch(self):
        result = PushEvent(self.json_string_develop)
        self.assertEqual(result.is_master(), False)

    def test_PushEvent_is_develop_returns_True_when_develop_branch(self):
        result = PushEvent(self.json_string_develop)
        self.assertEqual(result.is_develop(), True)

    def test_PushEvent_is_develop_returns_False_when_not_develop_branch(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.is_develop(), False)

    def test_PushEvent_is_feature_returns_True_when_feature_branch(self):
        result = PushEvent(self.json_string_feature)
        self.assertEqual(result.is_feature(), True)

    def test_PushEvent_is_feature_returns_False_when_not_feature_branch(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.is_feature(), False)

    def test_PushEvent_is_hotfix_returns_True_when_hotfix_branch(self):
        result = PushEvent(self.json_string_hotfix)
        self.assertEqual(result.is_hotfix(), True)

    def test_PushEvent_is_feature_returns_False_when_not_hotfix_branch(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.is_hotfix(), False)

    def test_PushEvent_commit_returns_commit_hash(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.commit, "1")

    def test_PushEvent_message_returns_commit_message(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.message, "test_message")

    def test_PushEvent_committer_returns_committer_of_commit(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.committer, "test_user")

    def test_PushEvent_pusher_returns_pusher_of_pusher(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.pusher, 'test_pusher')

    def test_PushEvent_url_returns_commit_url(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.url, "http://")

    def test_PushEvent_environment_variables_returns_str_of_variables(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.environment_variables,
                         'GIT_HASH=1\nGIT_MESSAGE="test_message"\n'
                         'GIT_AUTHOR=test_user\nGIT_PUSHER=test_pusher\n'
                         'GIT_URL=http://\nPUSHED_REPO=public-repo\n'
                         'PUSHED_BRANCH=master\nGIT_TYPE=master\nUAT_ON=false'
                         '\nPIPELINE_RUN=1\n')
