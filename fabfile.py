from contextlib import contextmanager
from functools import wraps
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

    templates = path.join(env.app, "source/templates/")
    env.maintenance_file = path.join(templates, "maintenance.html")

def log_call(func):
    @wraps(func)
    def logged(*args, **kawrgs):
        name = func.__name__.replace('_', ' ').title()
        line = "-" * len(name)
        out = ""

        for val in [name, line]:
            out += "\n   %s" % val
        print green(out)

        return func(*args, **kawrgs)
    return logged

def print_command(command):
    print "   %s %s %s\n" % (blue('$', bold=True),
                             yellow(command, bold=True),
                             red('->', bold=True))

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

def _maintenance(on=False):
    """ This will toggle maintenance mode on the server. """
    if on:
        sudo('ln -s %(maintenance_file)s %(public)s' % env)

    else:
        filepath = path.join(env.public, path.basename(env.maintenance_file))
        sudo('rm %s' % filepath)

    nginx("restart")

#################
# SPECIAL TASKS #
#################

@task
@log_call
def hostname(*args):
    """ This prints the hostname as a test. Use this to prime sudo by passing
    True.
    """
    if args and args[0] == "True":
        sudo("hostname")
    else:
        run("hostname")


@task
@log_call
def collect_static():
    """ Collects all of the static media. """
    return manage("collectstatic --noinput")


@task
@log_call
def install_requirements():
    """ Installs the requirements from the requirements.txt file. This will run
    as the deploy user if on dev.
    """
    with cd(env.app):
        return pip("install -r requirements.txt")


@task
@log_call
def migrate_db():
    """ Migrates the db. """
    return manage("migrate --all")


@task
@log_call
def pull():
    """ Git pulls on the remote host. """
    return git("pull")


@task
@log_call
def reload_nginx():
    """ Restarts the nginx process. """
    return nginx("reload")


@task
@log_call
def restart_django():
    """ Restarts the Django Supervisor process. """
    return supervisor("restart %(process)s" % env)


@task
@log_call
def restart_celery():
    """ Restarts the Celery Supervisor process. """
    return supervisor("restart celery")


@task
@log_call
def restart_memcached():
    """ Restarts the Memcached server. """
    return sudo("service memcached restart")


@task
@log_call
def clear_cache():
    """ Clears the cache. """
    return manage('clear_cache')


@task
@log_call
def begin_maintenance():
    """ Turns on maintenance mode. """
    _maintenance(on=True)


@task
@log_call
def end_maintenance():
    """ Turns off maintenance mode. """
    _maintenance(on=False)


@task
@log_call
def deploy(clear=False, maintenance=False, migrate=False, reload_nginx=False):
    """ Git pulls, installs requirements, collects static, then restarts
    django.
    """
    if maintenance:
        begin_maintenance()

    pull()
    install_requirements()
    collect_static()

    if clear:
        clear_cache()

    if migrate:
        migrate_db()

    restart_django()

    if maintenance:
        end_maintenance()

    elif reload_nginx:
        reload_nginx()
