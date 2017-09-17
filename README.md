# Git Timewarp

A command-line tool to modify commit timestamps in bulk.

## Example Commands

```bash
git-timewarp --help
git-timewarp randomize $REPO --earliest 0 --latest 23
git-timewarp standardize $REPO
git-timewarp strip $REPO --minutes --seconds
```

## Why?

This tool provides a quick way to obscure specific commit timestamps across a Git repo, while retaining the (more useful) overall commit chronology and date information.

This allows a developer to:

* Reduce their digital fingerprint of Git contributions when anonymity is desired
* Prank nosy coworkers by making all their commits late at night

## How to Run (Development)

First time only, set up your environment:

```bash
sudo apt-get install python3.6
python3.6 -m pip install virtualenv
python3.6 -m virtualenv venv
source venv/bin/activate
pip install click
deactivate
```

Each time you run the program, do this before / after.

```bash
source venv/bin/activate
deactivate
```

Testing the script as a CLI (within the venv):

```bash
pip install --editable .
git-timewarp --help
```

## References

* http://click.pocoo.org/5/quickstart/

## TODO

* Allow all commands to filter by author or email
* Allow all commands to filter for a single commit
* Allow all commands to filter by a range of commits
* Allow all commands to default to `.` if no repo specified
* Complete README doc with a sentence or two for each command
* 100% in pylint and mypy
* 90% in unit test coverage
