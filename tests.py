"""Tests for the gittimewarp program."""

from datetime import datetime
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
        newdate = gittimewarp.altered_commit_date(original, hour=0, minute=0, second=0)
        self.assertNotIn('00:00:00', original)
        self.assertIn('00:00:00', newdate)

    def test_set_commit_date(self):
        """Can set a single Git commit date in a repo to midnight."""
        commit = gittimewarp.all_commits(self.repo)[0]
        original = gittimewarp.get_commit_date(self.repo, commit)

        newdate = gittimewarp.altered_commit_date(original, hour=0, minute=0, second=0)
        gittimewarp.set_commit_date(self.repo, commit, newdate)

        new_commit = gittimewarp.all_commits(self.repo)[0]
        confirmation = gittimewarp.get_commit_date(self.repo, new_commit)
        self.assertIn('00:00:00', confirmation)


class TestWarpRepoTime(TempdirTestCase):
    """Can warp the time of an entire Git repo."""

    def setUp(self):
        super().setUp()
        gittimewarp.create_git_repo(self.tempdir, 'testrepo')
        self.repo = os.path.join(self.tempdir, 'testrepo')
        for _ in range(3):
            gittimewarp.create_dummy_commit(self.repo)

    def test_randomize_repo_times(self):
        """Can randomize times between hour-based boundaries."""
        gittimewarp.randomize_repo_times(self.repo, start=17, end=23)
        for commit in gittimewarp.all_commits(self.repo):
            timestamp = gittimewarp.get_commit_date(self.repo, commit)
            timestamp = ' '.join(timestamp.split()[:2])
            parsed = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            assert 17 <= parsed.hour <= 24

    def test_set_repo_times(self):
        """Can set commits to a specific time."""
        gittimewarp.set_repo_times(self.repo, hour=0, minute=1, second=2)
        for commit in gittimewarp.all_commits(self.repo):
            timestamp = gittimewarp.get_commit_date(self.repo, commit)
            timestamp = ' '.join(timestamp.split()[:2])
            parsed = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            assert parsed.hour == 0
            assert parsed.minute == 1
            assert parsed.second == 2
