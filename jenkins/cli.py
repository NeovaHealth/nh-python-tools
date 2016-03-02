# coding=utf-8
import sys

from optparse import OptionParser
from travis import TravisEvent
from branch import BranchPicker, PushEvent, GithubEvent, PullRequestEvent
from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-e', '--type', type=str, dest='trigger',
                  help='Even trigger type')
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub payload')
parser.add_option('-t', '--token', type=str, dest='token',
                  help='GitHub authorization token')


def set_github_event_type(options):
    event = GithubEvent(options.payload)
    if event.type == 'push':
        return PushEvent(event._payload)
    else:
        return PullRequestEvent(event._payload)


def github_environment_variables(options):
    event = set_github_event_type(options)
    repos = BranchPicker(
        event,
        [
            'nhclinical', 'openeobs', 'nh-mobile', 'nh-helpers',
            'nh-vmbuilder', 'nh-ansible', 'nh-playbooks', 'nh-vagrant',
            'openeobs-quality-assurance'
        ], options.token
    )
    return event.environment_variables + make_environment_variables(repos)


def travis_environment_variables(options):
    event = TravisEvent(options.payload)
    repos = BranchPicker(
        event,
        [
            'nhclinical', 'openeobs', 'nh-mobile', 'nh-helpers',
            'nh-vmbuilder', 'nh-ansible', 'nh-playbooks', 'nh-vagrant',
            'openeobs-quality-assurance'
        ], options.token
    )
    return event.environment_variables + make_environment_variables(repos)


if __name__ == '__main__':
    (options, args) = parser.parse_args()
    if options.trigger == 'travis':
        print travis_environment_variables(options)
    elif options.trigger == 'github':
        print github_environment_variables(options)
    else:
        print "Please supply trigger type '-e' - either 'travis' or 'github'"
    sys.exit()
