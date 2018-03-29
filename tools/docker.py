#!/usr/bin/env python
"""Work with Docker images."""

from os import environ
from subprocess import Popen
from sys import exit

import click


def run(cmd, ignore_err=False, **kwargs):
    proc = Popen(cmd, env=environ, **kwargs)
    try:
        proc.communicate()
    except KeyboardInterrupt:
        click.echo('Aborted!')
        exit(1)
    if proc.returncode and not ignore_err:
        exit(proc.returncode)


class Docker(object):

    def tags(self):
        yield 'latest'

    def build(self, name='my_image'):
        for cmd in self.command_base():
            yield cmd
        yield 'build'
        for tag in self.tags():
            yield '--tag'
            yield '{}:{}'.format(name, tag)
        yield '.'

    def command_base(self):
        """Yield the root of the docker command."""
        for cmd in ('sudo', '-E', 'docker'):
            yield cmd

    def stack_deploy(self, composefile, name):
        for cmd in self.command_base():
            yield cmd
        for cmd in (
                'stack',
                'deploy',
                '-c',
                composefile,
                name):
            yield cmd

    def swarm_init(self):
        for cmd in self.command_base():
            yield cmd
        for cmd in ('swarm', 'init'):
            yield cmd


def source(envfile):
    """Source an environment file specified in the args."""
    with open(envfile) as efile:
        for ln in (l.strip() for l in efile.readlines()):
            if not ln or ln.startswith('#') or '=' not in ln:
                continue
            key, val = ln.split('=', maxsplit=1)
            environ[key] = val


@click.group()
@click.option(
    '-e', '--envfile',
    default='.env',
    help='A file with environment variables to source'
)
def cli(envfile):
    """Perform Docker operations."""
    if envfile:
        source(envfile)


@cli.command()
@click.argument('image_name')
def build(image_name):
    """Build the Docker image."""
    run(Docker().build(image_name))


@cli.group()
@click.option(
    '--composefile',
    default='docker-compose.yml',
    help='docker compose file defining the stack'
)
@click.pass_context
def stack(ctx, composefile):
    ctx.obj = {'composefile': composefile}


@stack.command()
@click.option('--name', default='my_stack', help='the stack name')
@click.pass_context
def deploy(ctx, name):
    run(Docker().swarm_init(), ignore_err=True)
    run(Docker().stack_deploy(ctx.obj['composefile'], name))


@stack.command()
def init():
    run(Docker().swarm_init())


if __name__ == '__main__':
    cli()  # pylint: disable=E1120
