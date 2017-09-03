"""Command-line tool to modify Git repo timestamps in bulk."""

from datetime import datetime
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


def get_commit_date(repo: str, commit: str) -> str:
    """Return string format (for now) of a git commit timestamp."""
    result = git_command(['show', '-s', '--format=%ci', commit], folder=repo)
    return result.strip()


def altered_commit_datetime(commit_date: str, hour=0, minute=0, second=0) -> str:
    """Return string for adjusted commit datetime for use with alter command.
    commit_date argument has format from  `git show --format=%ci`.
    String returned has format for `git filter-branch export`.
    """
    date, time, timezone = commit_date.split()
    parsed = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    parsed = parsed.replace(hour=hour, minute=minute, second=second)
    return parsed.strftime('%a %b %-d %H:%M:%S %Y') + ' ' + timezone


@click.command()
@click.argument('repo')
@click.option('--start', default=17, help='Hour to start')
@click.option('--end', default=24, help='Hour to end')
def warp(repo: str, start: int, end: int):
    """Warp the time of all commits in a git repo."""
    click.echo(f'Warping... {repo} from {start} to {end}!')


if __name__ == '__main__':
    warp()
