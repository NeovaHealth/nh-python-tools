# coding=utf-8
import re


class Event(object):

    branch = None

    @property
    def type(self):
        if self.is_feature():
            return "feature"
        elif self.is_hotfix():
            return "hotfix"
        elif self.is_master():
            return "master"
        elif self.is_develop():
            return "develop"
        else:
            return "None"

    def is_hotfix(self):
        if re.match('[h][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False

    def is_feature(self):
        if re.match('[f][0-9]+_[a-z_0-9]{4,30}', self.branch):
            return True

        return False

    def is_master(self):
        if self.branch == 'master':
            return True

        return False

    def is_develop(self):
        if self.branch == 'develop':
            return True

        return False
