# coding=utf-8
import json

from unittest import TestCase

from jenkins.branch import RepoPush, PropertiesBuilder
from jenkins.utils import is_branch


class TestPushRepo(TestCase):

    def setUp(self):

        self.json_string = '{"ref": "refs/heads/master", "repository": ' \
                           '{"name": "public-repo"}}'
        self.json_string_develop = '{"ref": "refs/heads/develop", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_feature = '{"ref": "refs/heads/f1234_test", ' \
                                   '"repository": {"name": "public-repo"}}'
        self.json_string_hotfix = '{"ref": "refs/heads/h1234_test", ' \
                                  '"repository": {"name": "public-repo"}}'

    def test_PushRepo_has_instance_attributes_name_and_branch(self):
        result = RepoPush(self.json_string)

        self.assertEqual(result.name, 'public-repo')
        self.assertEqual(result.branch, 'master')

    def test_PushRepo_is_master_returns_True_when_master_branch(self):
        result = RepoPush(self.json_string)
        self.assertEqual(result.is_master(), True)

    def test_PushRepo_is_master_returns_False_when_not_master_branch(self):
        result = RepoPush(self.json_string_develop)
        self.assertEqual(result.is_master(), False)

    def test_PushRepo_is_feature_returns_True_when_feature_branch(self):
        result = RepoPush(self.json_string_feature)
        self.assertEqual(result.is_feature(), True)

    def test_PushRepo_is_feature_returns_False_when_not_feature_branch(self):
        result = RepoPush(self.json_string)
        self.assertEqual(result.is_feature(), False)

    def test_PushRepo_is_hotfix_returns_True_when_hotfix_branch(self):
        result = RepoPush(self.json_string_hotfix)
        self.assertEqual(result.is_hotfix(), True)

    def test_PushRepo_is_feature_returns_False_when_not_hotfix_branch(self):
        result = RepoPush(self.json_string)
        self.assertEqual(result.is_hotfix(), False)


class TestUtils(TestCase):

    def test_is_branch_returns(self):
        result = is_branch('develop', 'openeobs')
        self.assertEqual(result, True)

    def test_is_branch_returns_False_if_branch_does_not_exist(self):
        result = is_branch('test', 'openeobs')
        self.assertEqual(result, False)
