# Git Timewarp

A command-line tool to modify commit timestamps in bulk.

## Major Features

```
git-timewarp --help
git-timewarp -randomize ./my-repo --start 17 --end 24
```

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
