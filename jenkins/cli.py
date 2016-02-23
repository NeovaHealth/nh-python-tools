# coding=utf-8
import sys

from optparse import OptionParser
from branch import RepoPush, PropertiesBuilder
from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub push event payload')


def main():
    (options, args) = parser.parse_args()
    environment_variables = ""
    repo = RepoPush(options.payload)
    environment_variables += "TRIGGER_REPO=" + repo.name + "\n"
    environment_variables += "TRIGGER_BRANCH=" + repo.branch + "\n"
    repos = PropertiesBuilder(repo, ['nhclinical', 'openeobs', 'nh-mobile'])
    environment_variables += make_environment_variables(repos)
    print environment_variables


if __name__ == '__main__':
    sys.exit(main())
