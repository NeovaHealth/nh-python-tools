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
    repo = RepoPush(options.payload)
    repos = PropertiesBuilder(repo, ['nhclinical', 'openeobs', 'nh-mobile'])
    print make_environment_variables(repos)


if __name__ == '__main__':
    sys.exit(main())