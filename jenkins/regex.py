# coding=utf-8
import re


def regex_method(path):

    if (path):

        # Split path if string contains /'s
        if len(path.split('/')) > 1:
            branch = path.split('/')[-1]
        else:
            branch = path

        if branch == 'develop':
            return branch

        if branch == 'master':

            return branch
        # Catch incorrectly formatted strings
        if not re.match('[hf][0-9]+_[a-z_0-9]{4,30}', branch):
            print 'Branch name does not match regex'
            return False

        if re.match('[h]', branch):
            return 'hotfix'

        else:
            return 'feature'

    else:
        print 'No path argument provided'
        return False
