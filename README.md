# Git Timewarp

A command-line tool to modify commit timestamps in bulk.

## Major Features (work in progress)

```
git-timewarp --help
git-timewarp standardize ./my-repo
git-timewarp randomize ./my-repo --earliest 0 --latest 23
git-timewarp strip ./my-repo --minutes --seconds
git-timewarp shiftup ./my-repo --hours 3
```

## Why?

This tool will provide a quick way to obscure specific commit timestamps across a Git repo, while retaining the (more useful) overall commit chronology and date information.

This would allow:

* Reducing digital fingerprint when anonymity is required
* Screwing with nosy coworkers by making all your commits late at night


## How to Run

First time only, set up your environment:

```
sudo apt-get install python3.6
python3.6 -m pip install virtualenv
python3.6 -m virtualenv venv
source venv/bin/activate
pip install click
deactivate
```

Each time you run the program, do this before / after.

```
source venv/bin/activate
deactivate
```

Testing the script as a CLI (within the venv):

```
pip install --editable .
git-timewarp --help
```

## References

* http://click.pocoo.org/5/quickstart/
