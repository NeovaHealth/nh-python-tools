# coding=utf-8
from unittest import TestCase

from jenkins.regex import regex_method


class TestRegexLogic(TestCase):

    """
    Test that the webhook-receiver regex method correctly identifies feature
    and hotfix branches
    """

    def test_handles_paths_without_slashes(self):
        path = 'f111_feature'
        self.assertEqual(regex_method(path), 'feature')

    def test_handles_paths_with_only_1_slash(self):
        path = 'openeobs/h111_feature'
        self.assertEqual(regex_method(path), 'hotfix')

    def test_recognises_feature_branch_strings(self):
        path = 'origin/openeobs/f111_feature'
        self.assertEqual(regex_method(path), 'feature')

    def test_recognises_hotfix_branch_strings(self):
        path = 'origin/openeobs/h102_hotfixer'
        self.assertEqual(regex_method(path), 'hotfix')

    def test_returns_false_if_wrong_identifier_passed(self):
        path = 'origin/openeobs/d102_hotfixer'
        self.assertEqual(regex_method(path), False)

    def test_returns_false_if_contains_dash_characters(self):
        path = 'origin/openeobs/f102_hot-fixer'
        self.assertEqual(regex_method(path), False)

    def test_returns_false_if_incorrectly_formatted(self):
        path = 'origin/openeobs/f102hotfixer'
        self.assertEqual(regex_method(path), False)

    def test_returns_false_if_no_path_arg_provided(self):
        path = None
        self.assertEqual(regex_method(path), False)