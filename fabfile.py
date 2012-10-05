from os import path

from fabric.api import cd, env, hide, run as _run, sudo as _sudo, task
from fabric.colors import blue, green, red, yellow

env.use_ssh_config = True
env.colors = True

@task
def prod():
    env.hosts = ["twinsister"]
    env.deploy_user = None
    env.base = "/home/udbhav/www/django/eurorack-planner/"
    env.app = path.join(env.base, "app/")
    env.venv = path.join(env.base, "env/")
    env.process = "twinsister"
    env.public = path.join(env.base, "public/")

##############
# MAIN TASKS #
##############

@task
def run(command, show=True):
    """ Runs a shell command on the remote server. """
    if show:
        print_command(command)

    with hide("running"):
        if env.deploy_user:
            return _sudo(command, user=env.deploy_user)
        return _run(command)


@task
def sudo(command, show=True):
    """ Runs a command as sudo. """
    if show:
        print_command(command)

    with hide("running"):
        return _sudo(command)


@task
def python(command):
    """ Runs a command with the environment's python binary. """
    _python = path.join(env.venv, "bin/python")
    return run("%s %s" % (_python, command))


@task
def manage(command):
    """ Run a django management command. """
    with cd(path.join(env.app, "source/")):
        return python("manage.py %s" % command)


@task
def git(command):
    """ Run a git command on the remote server. """
    with cd(env.app):
        return run("git %s" % command)


@task
def pip(command):
    """ Runs pip in the environment with the given command. """
    _pip = path.join(env.venv, "bin/pip")
    return run("%s %s" % (_pip, command))


@task
def nginx(command):
    """ Runs an Nginx command. """
    return sudo("service nginx %s" % command)


@task
def supervisor(command):
    """ Runs an supervisor command. """
    return sudo("supervisorctl %s" % command)
