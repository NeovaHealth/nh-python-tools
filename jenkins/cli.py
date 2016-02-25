# coding=utf-8
import sys

from optparse import OptionParser
from branch import PushEvent, PropertiesBuilder
from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub push event payload')


def main():
    (options, args) = parser.parse_args()
    repo = PushEvent(options.payload)
    repos = PropertiesBuilder(
        repo, ['nhclinical', 'openeobs', 'nh-mobile', 'nh-helpers'])
    print repo.environment_variables + make_environment_variables(repos)


if __name__ == '__main__':
    sys.exit(main())