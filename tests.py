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


class TestCreateGitRepo(TempdirTestCase):
    """Can create a git repo with dummy commits for testing."""

    def test_create_repo(self):
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        repo = os.path.join(self.tempdir, 'testrepo')
        self.assertTrue(os.path.exists(repo))

    def test_dummy_commit(self):
        """Test creation of dummy commits.
        Also test ability to get number of and list of commits.
        """
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        repo = os.path.join(self.tempdir, 'testrepo')

        for _ in range(3):
            gittimewarp.create_dummy_commit(repo)

        self.assertEqual(gittimewarp.number_git_commits(repo), 3)
        self.assertEqual(len(gittimewarp.all_commits(repo)), 3)


class TestAlterCommitTime(TempdirTestCase):
    """Can alter the time of a commit in a Git repo."""

    def setUp(self):
        super().setUp()
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        self.repo = os.path.join(self.tempdir, 'testrepo')
        gittimewarp.create_dummy_commit(self.repo)

    def test_altered_datetime(self):
        """Can get new datetime (midnight) from a current Git commit."""
        original = gittimewarp.get_commit_date(self.repo, gittimewarp.all_commits(self.repo)[0])
        newdate = gittimewarp.altered_commit_datetime(original)
        self.assertNotIn('00:00:00', original)
        self.assertIn('00:00:00', newdate)

    def test_set_commit_date(self):
        """Can set a single Git commit date in a repo to midnight."""
        commit = gittimewarp.all_commits(self.repo)[0]
        original = gittimewarp.get_commit_date(self.repo, commit)

        newdate = gittimewarp.altered_commit_datetime(original)
        gittimewarp.set_commit_date(self.repo, commit, newdate)

        new_commit = gittimewarp.all_commits(self.repo)[0]
        confirmation = gittimewarp.get_commit_date(self.repo, new_commit)
        self.assertIn('00:00:00', confirmation)
