# coding=utf-8
from unittest import TestCase

from jenkins.travis import TravisEvent


class TestTravisEvent(TestCase):

    def setUp(self):
        self.json_payload = '{"branch": "master", "type": "push", ' \
                            '"commit": "62aae5f70ceee39123ef", ' \
                            '"message": "test message", ' \
                            '"committer_name": "John Smith", ' \
                            '"repository": {"name": "test_repo", ' \
                            '"url": "http://test_url.com"}}'
        self.json_develop = '{"branch": "develop"}'
        self.json_master = '{"branch": "master"}'
        self.json_hotfix = '{"branch": "h1234_test"}'
        self.json_feature = '{"branch": "f1234_test"}'
        self.json_other = '{"branch": "other"}'

    def test_TravisEvent_has_expected_properties(self):
        result = TravisEvent(self.json_payload)

        self.assertEqual(result.name, 'test_repo')
        self.assertEqual(result.branch, 'master')
        self.assertEqual(result.commit, '62aae5f70ceee39123ef')

    def test_TravisEvent_type_returns_type_of_branch(self):
        result = TravisEvent(self.json_master)
        self.assertEqual(result.is_master(), True)

    def test_TravisEvent_is_master_returns_False_if_not_master_branch(self):
        result = TravisEvent(self.json_develop)
        self.assertEqual(result.is_master(), False)

    def test_TravisEvent_is_develop_returns_True_if_develop_branch(self):
        result = TravisEvent(self.json_develop)
        self.assertEqual(result.is_develop(), True)

    def test_TravisEvent_is_develop_returns_False_if_not_develop_branch(self):
        result = TravisEvent(self.json_master)
        self.assertEqual(result.is_develop(), False)

    def test_TravisEvent_is_feature_returns_True_if_feature_branch(self):
        result = TravisEvent(self.json_feature)
        self.assertEqual(result.is_feature(), True)

    def test_TravisEvent_is_feature_returns_False_if_not_feature_branch(self):
        result = TravisEvent(self.json_master)
        self.assertEqual(result.is_feature(), False)

    def test_TravisEvent_is_hotfix_returns_True_if_hotfix_branch(self):
        result = TravisEvent(self.json_hotfix)
        self.assertEqual(result.is_hotfix(), True)

    def test_TravisEvent_is_feature_returns_False_if_not_hotfix_branch(self):
        result = TravisEvent(self.json_master)
        self.assertEqual(result.is_hotfix(), False)

