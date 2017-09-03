"""Command-line tool to modify Git repo timestamps in bulk."""

import os
from subprocess import Popen, PIPE
from typing import List

import click


class GitError(Exception):
    pass


def git_command(parts: list, folder: str):
    """Run a git command in a directory.
    Raise a GitError if this fails.
    Return the result as a decoded string if it succeeds.
    """
    command = ['/usr/bin/git'] + parts
    process = Popen(command, cwd=folder, stdout=PIPE, stderr=PIPE)

    result, error = process.communicate()
    if error:
        raise GitError(error.decode())

    return result.decode()


def create_git_repo(folder: str, name: str):
    """Create a git repo at folder with name.
    Raise a GitError if this fails.
    """
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass

    result = git_command(['init', name], folder=folder)

    if not result.startswith('Initialized empty Git repo'):
        raise GitError(f'Bad result: {result}')


def number_git_commits(repo: str):
    """Return number of commits in a Git repo."""
    try:
        count = git_command('rev-list --all --count .'.split(), repo)
    except GitError:
        return 0
    else:
        return int(count.strip())


def create_dummy_commit(repo: str):
    """Create a commit at current time in a Git repo.
    Raise a GitError if this fails.
    """
    count_commits = number_git_commits(repo)

    dummy = os.path.join(repo, 'dummy.txt')
    with open(dummy, 'a') as stream:
        stream.write(' ')
    git_command(['add', 'dummy.txt'], folder=repo)
    git_command(['commit', '-m', 'dummy commit'], folder=repo)

    new_count_commits = number_git_commits(repo)
    assert new_count_commits - count_commits == 1


def all_commits(repo: str) -> List[str]:
    """Return list of all commit hashes in chronological order.
    Raise a GitError if this fails.
    """
    results = git_command(['log', '--pretty=format:%h'], folder=repo)
    commits = results.strip().split('\n')
    return commits


def alter_commit_time(repo: str, commit: str, hour=0):
    """Alter the time of a commit in a repo.
    'hour' must be an integer from 0 to 23 (for now).
    """
    pass


@click.command()
@click.argument('repo')
@click.option('--start', default=17, help='Hour to start')
@click.option('--end', default=24, help='Hour to end')
def warp(repo: str, start: int, end: int):
    """Warp the time of all commits in a git repo."""
    click.echo(f'Warping... {repo} from {start} to {end}!')


if __name__ == '__main__':
    warp()
