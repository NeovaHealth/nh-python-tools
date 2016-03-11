# coding=utf-8
from unittest import TestCase

from jenkins.event import Event


class TestEvent(TestCase):

    def setUp(self):
        self.event = Event()

    def test_Event_is_master_returns_True_when_master_branch(self):
        self.event.branch = 'master'
        self.assertEqual(self.event.is_master(), True)

    def test_Event_is_master_returns_False_when_not_master_branch(self):
        self.event.branch = 'not_master'
        self.assertEqual(self.event.is_master(), False)

    def test_Event_is_develop_returns_True_when_develop_branch(self):
        self.event.branch = 'develop'
        self.assertEqual(self.event.is_develop(), True)

    def test_Event_is_develop_returns_False_when_not_develop_branch(self):
        self.event.branch = 'not_develop'
        self.assertEqual(self.event.is_develop(), False)

    def test_Event_is_feature_returns_True_when_feature_branch(self):
        self.event.branch = 'f1234_test'
        self.assertEqual(self.event.is_feature(), True)

    def test_Event_is_feature_returns_False_when_not_feature_branch(self):
        self.event.branch = 'not_feature'
        self.assertEqual(self.event.is_feature(), False)

    def test_Event_is_hotfix_returns_True_when_hotfix_branch(self):
        self.event.branch = 'h1234_test'
        self.assertEqual(self.event.is_hotfix(), True)

    def test_Event_is_feature_returns_False_when_not_hotfix_branch(self):
        self.event.branch = 'not_hotfix'
        self.assertEqual(self.event.is_hotfix(), False)

    def test_type_returns_feature_when_branch_is_a_feature_branch(self):
        self.event.branch = 'f1234_test'
        self.assertEqual(self.event.type, 'feature')

    def test_type_returns_hotfix_when_branch_is_a_hotfix_branch(self):
        self.event.branch = 'h1234_test'
        self.assertEqual(self.event.type, 'hotfix')

    def test_type_returns_master_when_branch_is_a_master_branch(self):
        self.event.branch = 'master'
        self.assertEqual(self.event.type, 'master')

    def test_type_returns_develop_when_branch_is_a_develop_branch(self):
        self.event.branch = 'develop'
        self.assertEqual(self.event.type, 'develop')

    def test_type_returns_None_string_when_branch_type_is_unknown(self):
        self.event.branch = 'no type'
        self.assertEqual(self.event.type, 'None')

