"""Tests for the gittimewarp program."""

import shutil
import os
import tempfile
import unittest

import gittimewarp


class TempdirTestCase(unittest.TestCase):
    """A TestCase with a tempdir that deletes afterward."""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)


class TestInitGitRepo(TempdirTestCase):
    """Can initialize a git repo for testing."""

    def test_create_repo(self):
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        repo = os.path.join(self.tempdir, 'testrepo')
        self.assertTrue(os.path.exists(repo))

    def test_dummy_commit(self):
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        repo = os.path.join(self.tempdir, 'testrepo')
        gittimewarp.create_dummy_commit(repo)


class TestWarpGitRepo(TempdirTestCase):
    """Can warp the time of all commits in a repo to midnight."""

    def setUp(self):
        super().setUp()
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        self.repo = os.path.join(self.tempdir, 'testrepo')
        # for _ in range(5):
        gittimewarp.create_dummy_commit(self.repo)

    def test_warp(self):
        pass
