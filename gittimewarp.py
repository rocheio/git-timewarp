"""Command-line tool to modify Git repo timestamps in bulk."""

from datetime import datetime
import os
import random
from subprocess import Popen, PIPE
from typing import List

import click


class GitError(Exception):
    pass


class InvalidTimeFormat(Exception):
    pass


def git_command(parts: list, folder: str):
    """Run a git command in a directory.
    Raise a GitError if this fails.
    Return the result as a decoded string if it succeeds.
    """
    command = ['/usr/bin/git'] + parts
    process = Popen(command, cwd=folder, stdout=PIPE, stderr=PIPE)

    result, error = process.communicate()
    if error and 'WARNING' not in error.decode():
        raise GitError(error.decode())

    return result.decode().strip()


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
    """Return list of all commit hashes in REVERSE chronological order.
    Raise a GitError if this fails.
    """
    results = git_command(['log', '--pretty=format:%H'], folder=repo)
    commits = results.split('\n')
    return commits


def get_commit_date(repo: str, commit: str) -> str:
    """Return string format (for now) of a git commit timestamp."""
    result = git_command(['show', '-s', '--format=%ci', commit], folder=repo)
    return result


def set_commit_date(repo: str, commit: str, new_date: str):
    """Convert the auther and commit dates of a commit in a repo."""
    command = [
        'filter-branch', '-f', '--env-filter',
        f"""
        if [ $GIT_COMMIT = {commit} ];
        then
            export GIT_AUTHOR_DATE="{new_date}";
            export GIT_COMMITTER_DATE="{new_date}";
        fi
        """.strip()
    ]
    result = git_command(command, repo)
    if result.endswith('was rewritten'):
        return
    if result.endswith('remaining 0 predicted)'):
        return
    raise GitError(f'Unexpected git result: {result}')


def altered_commit_date(commit_date: str, hour: int = None,
                        minute: int = None, second: int = None) -> str:
    """Return string for adjusted commit datetime for use with alter command.
    commit_date argument has format from  `git show --format=%ci`.
    String returned has format for `git filter-branch export`.
    """
    date, time, timezone = commit_date.split()
    parsed = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
    parsed = parsed.replace(hour=hour, minute=minute, second=second)
    return parsed.strftime('%a, %d %b %Y %H:%M:%S') + ' ' + timezone


def randomize_repo_times(repo: str, start=0, end=23, echo=True):
    """Randomize all commit times in a repo between hour boundaries."""
    if not 0 <= start <= 23 or not isinstance(start, int):
        raise InvalidTimeFormat('start must be an integer between 0 and 23')

    if not 0 <= end <= 23 or not isinstance(end, int):
        raise InvalidTimeFormat('end must be an integer between 0 and 23')

    for commit in all_commits(repo):
        current_date = get_commit_date(repo, commit)
        hour = random.randint(start, end)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        altered = altered_commit_date(current_date, hour=hour,
                                      minute=minute, second=second)
        if echo:
            click.echo(f'Changing commit {commit[:10]} date from '
                       f'{current_date} to {altered}')
        set_commit_date(repo, commit, altered)


def set_repo_times(repo: str, hour=0, minute=0, second=0, echo=True):
    """Randomize all commit times in a repo between hour boundaries."""
    if not 0 <= hour <= 23 or not isinstance(hour, int):
        raise InvalidTimeFormat('hour must be an integer between 0 and 23')

    if not 0 <= minute <= 59 or not isinstance(minute, int):
        raise InvalidTimeFormat('minute must be an integer between 0 and 59')

    if not 0 <= second <= 59 or not isinstance(second, int):
        raise InvalidTimeFormat('second must be an integer between 0 and 59')

    for commit in all_commits(repo):
        current_date = get_commit_date(repo, commit)
        altered = altered_commit_date(current_date, hour=hour,
                                      minute=minute, second=second)
        if echo:
            click.echo(f'Changing commit {commit[:10]} date from '
                       f'{current_date} to {altered}')
        set_commit_date(repo, commit, altered)


@click.group()
def cli():
    """Modify the timestamp of every commit in a Git repo."""
    pass


@cli.command()
@click.argument('repo')
@click.option('--earliest', default=0, help='Earliest hour for altered commits.')
@click.option('--latest', default=23, help='Latest hour for altered commits.')
def randomize(repo: str, earliest: int, latest: int):
    """Randomize time of all commits."""
    repo = os.path.abspath(repo)
    message = f'Randomize all commit times in "{repo}" from {earliest} to {latest}?'
    if not click.confirm(message):
        return
    randomize_repo_times(repo, earliest, latest)
    click.echo('Finished randomizing commit times.')


@cli.command()
@click.argument('repo')
@click.option('--hour', default=0, help='New hour for altered commits.')
def standardize(repo: str, hour: int):
    """Set time of all commits to the same value."""
    repo = os.path.abspath(repo)
    newtime = datetime.strptime(str(hour), '%H').time()
    count = number_git_commits(repo)
    message = f'Set all {count} commit times in "{repo}" to {newtime}?'
    if not click.confirm(message):
        return
    set_repo_times(repo, hour)
    click.echo('Finished standardizing commit times.')


@cli.command()
@click.argument('repo')
@click.option('--hours', default=False, help='Replace hour values?')
@click.option('--minutes', default=False, help='Replace minute values?')
@click.option('--seconds', default=False, help='Replace second values?')
def strip(repo: str, hours: bool, minutes: bool, seconds: bool):
    """Set time unit(s) to 0 for all commits."""
    if not any(hours, minutes, seconds):
        click.echo(f'No time units (hours, minutes, seconds) specified for removal')
        return

    click.echo('Stripping selected time unit(s) from git commits')

    # Determine which time fields to replace with zero
    hour = 0 if hours else None
    minute = 0 if minutes else None
    second = 0 if seconds else None

    for commit in all_commits(repo):
        current_date = get_commit_date(repo, commit)
        altered = altered_commit_date(current_date, hour=hour,
                                      minute=minute, second=second)
        set_commit_date(repo, commit, altered)
