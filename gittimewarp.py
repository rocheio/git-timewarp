"""Command-line tool to modify Git repo timestamps in bulk."""

import os
import sys

import click


@click.command()
@click.argument('repo')
@click.option('--start', default=17, help='Hour to start')
@click.option('--end', default=24, help='Hour to end')
def warp(repo: str, start: int, end: int):
    """Warp the time of all commits in a git repo."""
    click.echo(f'Warping... {repo} from {start} to {end}!')


if __name__ == '__main__':
    warp()
