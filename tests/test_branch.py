# coding=utf-8
from unittest import TestCase

from jenkins.branch import get_branch, is_branch, get_repos


class TestBranch(TestCase):

    def test_get_branch_returns_a_dict_with_repo_and_branch_keys(self):
        with open('payload.json') as payload:
            result = get_branch(payload)
            self.assertEqual(result['repository'], 'public-repo')
            self.assertEqual(result['branch'], 'changes')

    def test_is_branch_returns(self):
        result = is_branch('develop', 'openeobs')
        self.assertEqual(result, True)

    def test_is_branch_returns_False_if_branch_does_not_exist(self):
        result = is_branch('test', 'openeobs')
        self.assertEqual(result, False)

    def test_get_repos_on_openeobs_develop(self):
        result = get_repos({'repository': 'openeobs', 'branch': 'develop'})
        self.assertEqual({'nh-mobile': 'master', 'nhclinical': 'develop',
                          'openeobs': 'develop'}, result)

    def test_get_repos_on_openeobs_master(self):
        result = get_repos({'repository': 'openeobs', 'branch': 'master'})
        self.assertEqual({'nh-mobile': 'master', 'nhclinical': 'master',
                          'openeobs': 'master'}, result)