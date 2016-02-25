# coding=utf-8
from unittest import TestCase

from jenkins.branch import PushEvent, PropertiesBuilder, Repository_new
from jenkins.utils import is_branch


class Tes_PushEvent(TestCase):

    def setUp(self):

        self.json_string = '{"ref": "refs/heads/master", "repository": ' \
                           '{"name": "public-repo"}, "head_commit": ' \
                           '[{"id": "1", "message": "test_message", ' \
                           '"committer": {"username": "test_user"}, ' \
                           '"url": "http://"}]}'

        self.json_string_develop = '{"ref": "refs/heads/develop", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_feature = '{"ref": "refs/heads/f1234_test", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_hotfix = '{"ref": "refs/heads/h1234_test", ' \
                                  '"repository": {"name": "public-repo"}}'

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

    def test_PushEvent_url_returns_commit_url(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.url, "http://")

    def test_PushEvent_environment_variables_returns_str_of_variables(self):
        result = PushEvent(self.json_string)
        self.assertEqual(result.environment_variables,
                         'GIT_HASH=1\nGIT_MESSAGE=test_message\n'
                         'GIT_AUTHOR=test_user\nGIT_URL=http://\n'
                         'GIT_REPO=public-repo\nGIT_BRANCH=master\n'
                         'GIT_TYPE=master\n')


class TestRepository(TestCase):

    def setUp(self):
        self.json_string = '{"ref": "refs/heads/master", "repository": ' \
                           '{"name": "public-repo"}}'
        self.push = PushEvent(self.json_string)

    def test_repository(self):
        r = Repository_new.create_repository_from_push_event(self.push)
        self.assertEqual(r.name, 'public-repo')

    def test_environment_variables(self):
        r = Repository_new('test_name', 'test_branch')
        self.assertEqual(r.environment_variable, 'TESTNAME_BRANCH')


class TestUtils(TestCase):

    def test_is_branch_returns(self):
        result = is_branch('develop', 'openeobs')
        self.assertEqual(result, True)

    def test_is_branch_returns_False_if_branch_does_not_exist(self):
        result = is_branch('test', 'openeobs')
        self.assertEqual(result, False)
