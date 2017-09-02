from setuptools import setup

setup(
    name='git-timewarp',
    version='0.1',
    py_modules=['git-timewarp'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        git-timewarp=gittimewarp:warp
    ''',
)
