"""Tests for the gittimewarp program.""" 

import shutil
from subprocess import Popen, PIPE
import sys
import os
import tempfile
import unittest


class TestInitGitRepo(unittest.TestCase):
    """Can initialize a git repo for testing."""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_create_repo(self):
        try:
            os.mkdir(self.tempdir)
        except FileExistsError:
            pass

        command = ['/usr/bin/git', 'init', 'testrepo']
        process = Popen(command, cwd=self.tempdir, stdout=PIPE, stderr=PIPE)

        result, error = process.communicate()

        # Repo created, and no errors
        success = result.decode().startswith('Initialized empty Git repo')
        self.assertTrue(success)
        self.assertFalse(error)
