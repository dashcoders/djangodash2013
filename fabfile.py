# coding: utf-8
import os
from fabric.api import env, sudo
from fabric.colors import green


PROJECT_USER = 'forgetmyex'
PROJECT_ROOT = '/home/{project_user}/project/'.format(project_user=PROJECT_USER)
VIRTUALENV_ROOT = '/home/{project_user}/_env/'.format(project_user=PROJECT_USER)
MANAGE_PY_PATH = '/home/{project_user}/project/django/app/manage.py'.format(project_user=PROJECT_USER)
REQUIREMENTS_PATH = '/home/{project_user}/project/django/requirements.txt'.format(project_user=PROJECT_USER)
REPOSITORY_TYPE = 'git'


env.environment_name = None
env.hosts = []
env.user = 'ubuntu'


class require_environment(object):
    def __init__(self, method):
        self.method = method

    def __call__(self, *args, **kwargs):
        if not env.environment_name:
            raise Exception('No environment was selected. Please call: fab (sandbox|production) [yourcommand yourcommand2]')

        str_args = ','.join(["'{arg}'".format(arg=arg) if ' ' in arg else arg for arg in args])
        str_kwargs = ','.join(['{0}={1}'.format(i[0], "'{arg}'".format(arg=i[1]) if ' ' in i[1] else i[1]) for i in kwargs.items()])
        str_extra = ':' if str_args or str_kwargs else ''
        command = '{method_name}{str_extra}{str_args}{str_kwargs}'.format(
            method_name=self.method.func_name,
            str_extra=str_extra,
            str_args=str_args,
            str_kwargs=str_kwargs,
        )

        print green('Executing: {command}'.format(command=command))
        return self.method(*args, **kwargs)


# environments
def production():
    env.environment_name = 'production'
    env.hosts = [
        'forgetmyex.co',
    ]


def sandbox():
    raise NotImplementedError()


# commands
@require_environment
def deploy():
    update_source()

    update_dependencies()

    if not getattr(env, 'collectstatic_executed', False):
        env.collectstatic_executed = True
        manage_py('collectstatic --noinput')

    manage_py('compress')

    restart_services()


@require_environment
def update_source():
    if REPOSITORY_TYPE in ['git']:
        pull_command = 'git pull'
    elif REPOSITORY_TYPE in ['mercurial', 'hg']:
        pull_command = 'hg pull -u'
    else:
        raise NotImplementedError()

    command = 'su -l {project_user} -c "cd {project_root} && {pull_command}"'.format(
        project_user=PROJECT_USER,
        project_root=PROJECT_ROOT,
        pull_command=pull_command,
    )
    sudo(command)


@require_environment
def manage_py(command):
    python_path = os.path.join(VIRTUALENV_ROOT, 'bin', 'python')
    settings = 'settings.{environment_name}'.format(environment_name=env.environment_name)
    command = 'su -l {project_user} -c "{python_path} {manage_py_path} {command} --settings={settings}"'.format(
        project_user=PROJECT_USER,
        python_path=python_path,
        manage_py_path=MANAGE_PY_PATH,
        command=command,
        settings=settings,
    )
    sudo(command)


@require_environment
def update_dependencies():
    pip_path = os.path.join(VIRTUALENV_ROOT, 'bin', 'pip')
    command = 'su -l {project_user} -c "{pip_path} install -r {requirements_path}"'.format(
        project_user=PROJECT_USER,
        pip_path=pip_path,
        manage_py_path=MANAGE_PY_PATH,
        requirements_path=REQUIREMENTS_PATH,
    )
    sudo(command)


@require_environment
def restart_services():
    sudo('supervisorctl restart all')
