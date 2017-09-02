"""Command-line tool to modify Git repo timestamps in bulk."""

import os
from subprocess import Popen, PIPE

import click


class GitError(Exception):
    pass


def create_git_repo(folder: str, name: str):
    """Create a git repo at folder with name.
    Raise a GitError if the repo cannot be created.
    """
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    command = ['/usr/bin/git', 'init', name]
    process = Popen(command, cwd=folder, stdout=PIPE, stderr=PIPE)

    result, error = process.communicate()

    if not result.decode().startswith('Initialized empty Git repo'):
        raise GitError(f'Bad result: {result}')

    if error:
        raise GitError(error)


@click.command()
@click.argument('repo')
@click.option('--start', default=17, help='Hour to start')
@click.option('--end', default=24, help='Hour to end')
def warp(repo: str, start: int, end: int):
    """Warp the time of all commits in a git repo."""
    click.echo(f'Warping... {repo} from {start} to {end}!')


if __name__ == '__main__':
    warp()
