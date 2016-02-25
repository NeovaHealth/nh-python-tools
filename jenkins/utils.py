# coding=utf-8


def make_environment_variables(builders):
    """Constructs environment variables string."""
    variables = ""
    for repository in builders.repositories:
        if repository.name == 'nhclinical':
            variables += "NHC_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'openeobs':
            variables += "OE_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-mobile':
            variables += "NHM_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-helpers':
            variables += "HELPERS_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-vmbuilder':
            variables += "VMBUILDER_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-ansible':
            variables += "ANSIBLE_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-playbook':
            variables += "PLAYBOOK_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'nh-vagrant':
            variables += "VAGRANT_BRANCH=" + repository.branch + "\n"
        elif repository.name == 'openeobs-quality-assurance':
            variables += "QA_BRANCH=" + repository.branch + "\n"

    return variables


