# coding=utf-8
import sys

from optparse import OptionParser
from branch import PushEvent, PropertiesBuilder
from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-p', '--payload', dest='payload', metavar="FILE",
                  help='GitHub push event payload')
parser.add_option('-t', '--token', type=str, dest='token',
                  help='GitHub authorization token')


def main():
    (options, args) = parser.parse_args()
    repo = PushEvent(options.payload)
    repos = PropertiesBuilder(
        repo,
        [
            'nhclinical', 'openeobs', 'nh-mobile', 'nh-helpers',
            'nh-vmbuilder', 'nh-ansible', 'nh-playbooks', 'nh-vagrant',
            'openeobs-quality-assurance'
        ], options.token
    )
    print repo.environment_variables + make_environment_variables(repos)


if __name__ == '__main__':
    sys.exit(main())