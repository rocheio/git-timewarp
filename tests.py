"""Tests for the gittimewarp program."""

import shutil
import os
import tempfile
import unittest

import gittimewarp


class TestInitGitRepo(unittest.TestCase):
    """Can initialize a git repo for testing."""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_create_repo(self):
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        repo = os.path.join(self.tempdir, 'testrepo')
        self.assertTrue(os.path.exists(repo))


class TestWarpGitRepo(unittest.TestCase):
    """Can warp the time of all commits in a repo to midnight."""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        self.repo = os.path.join(self.tempdir, 'testrepo')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_warp(self):
        pass
