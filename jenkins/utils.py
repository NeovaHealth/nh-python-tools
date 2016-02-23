# coding=utf-8
import urllib2


def make_environment_variables(builders):
    variables = ""
    for repository in builders.repositories:
        if repository.name == 'nhclinical':
            variables += "NHC_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'openeobs':
            variables += "OE_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-mobile':
            variables += "NHM_BRANCH=" + repository.branch + "\n"

    return variables


def is_branch(branch_name, repository):
    """Checks if repository has a given remote branch."""
    url = "https://api.github.com/repos/NeovaHealth/" + repository + \
          "/branches/" + branch_name
    try:
        urllib2.urlopen(url)
    except urllib2.HTTPError:
        result = False
    else:
        result = True
    return result
