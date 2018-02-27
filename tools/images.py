"""Work with Docker images."""

from argparse import ArgumentParser
from os import environ


class Arguments:
    """Simple argparse wrapper."""

    def __init__(self):
        self.parser = ArgumentParser()
        self.setup(self.parser)

    @staticmethod
    def setup(parser):
        """Set up parsers.

        :param ArgumentParser parser: the parser to setup
        :rtype: None
        """
        subparsers = parser.add_subparsers(title='subcommands', dest='command')
        subparsers.add_parser('build')
        subparsers.add_parser('push')

    @staticmethod
    def setup_build(parser):
        """Set up the build parser.

        :param argparse.ArgumentParser parser: the parser to setup
        :rtype: None
        """
        parser.add_argument(
            '-d',
            '--dockerfile',
            default='Dockerfile',
            help=(
                'Path to Dockerfile, relative to working directory or '
                'absolute. Default is "Dockerfile"'
            )
        )
        parser.add_argument(
            '--context',
            default='.',
            help=(
                'Path to docker build context, relative to working directory '
                'or absolute. Default is "."'
            )
        )

    @staticmethod
    def setup_root(parser):
        """Set up the root parser.

        :param argparse.ArgumentParser parser: the parser to setup
        :rtype: None
        """
        parser.add_argument(
            '-e',
            '--envfile',
            default='../.envrc',
            help=(
                'The environment file to source. Relative paths are relative'
                'to the present working directory. Default is ".envrc".'
            )
        )
        parser.add_argument(
            '--no-sudo',
            action='store_true',
            help='Do not prefix Docker commands with "sudo".'
        )

    def parse(self):
        """Parse command-line arguments.

        :rtype: argparse.Namespace
        """
        return self.parser.parse_args()


class Docker:

    def __init__(self, arguments):
        self.args = arguments

    def build(self):
        # TODO: continue here (dev versioning needed also)
        pass

    def command_base(self):
        """Yield the root of the docker command."""
        if not self.args.no_sudo:
            yield 'sudo'
        yield 'docker'


class Images:

    def __init__(self, arguments):
        self.args = arguments

    def source(self):
        """Source an environment file specified in the args."""
        with open(self.args.envfile) as envfile:
            for ln in (l.strip() for l in envfile.readlines()):
                if not ln or ln.startswith('#') or not '=' in ln:
                    continue
                key, val = ln.split('=', maxsplit=1)
                environ[key] = val

    def build(self):
        pass

    def run_subcommand(self):
        """Run the subcommand specified in the arguments.

        :raises AttributeError: if the requested command does not exist
        """
        cmd = getattr(self, self.args.command)
        return cmd()

    def push(self):
        pass


def main():
    """Perform the requested action."""
    arguments = Arguments()
    args = arguments.parse()
    images = Images(args)
    try:
        commands.run_subcommand()
    except AttributeError:
        arguments.parser.print_help()


if __name__ == '__main__':
    main()
