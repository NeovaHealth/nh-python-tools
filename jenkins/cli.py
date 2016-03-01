# coding=utf-8
import sys

from optparse import OptionParser
from travis import TravisEvent
from branch import PropertiesBuilder, PushEvent, GithubEvent, PullRequestEvent
from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-e', '--type', type=str, help='Even trigger type', dest='trigger')
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub payload')
parser.add_option('-t', '--token', type=str, dest='token',
                  help='GitHub authorization token')



def github(options):
    event = GithubEvent(options.payload)
    repo = PushEvent(event._payload) if event.type == 'push' else PullRequestEvent(event._payload)

    repos = PropertiesBuilder(
        repo,
        [
            'nhclinical', 'openeobs', 'nh-mobile', 'nh-helpers',
            'nh-vmbuilder', 'nh-ansible', 'nh-playbooks', 'nh-vagrant',
            'openeobs-quality-assurance'
        ], options.token
    )
    print repo.environment_variables + make_environment_variables(repos)


def travis(options):
    repo = TravisEvent(options.payload)
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
    (options, args) = parser.parse_args()
    if options.trigger == 'travis':
        sys.exit(travis(options))
    elif options.trigger == 'github':
        sys.exit(github(options))
    else:
        print "Please supply trigger type '-e' - either 'travis' or 'github'"
        sys.exit()
