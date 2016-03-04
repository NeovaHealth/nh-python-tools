# coding=utf-8
import sys
import json

from optparse import OptionParser
from travis import TravisEvent
from github import github_event_factory
from branch import BranchPicker

from utils import make_environment_variables


parser = OptionParser()
parser.add_option('-e', '--type', type=str, dest='trigger',
                  help='Even trigger type')
parser.add_option('-p', '--payload', type=str, dest='payload',
                  help='GitHub payload')
parser.add_option('-t', '--token', type=str, dest='token',
                  help='GitHub authorization token')


def github_environment_variables(options):
    payload = json.loads(options.payload)
    event = github_event_factory(payload)
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
    payload = json.loads(options.payload)
    event = TravisEvent(payload)
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
