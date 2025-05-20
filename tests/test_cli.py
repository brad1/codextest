import os
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import sys
import tempfile
from pathlib import Path

import cli


class TestCLI(unittest.TestCase):
    def test_no_arguments_shows_usage(self):
        """GIVEN no arguments
        WHEN main is called
        THEN it should print usage and exit with code 0"""
        buf = io.StringIO()
        with patch.object(sys, 'argv', ['cli.py']):
            with redirect_stdout(buf):
                code = cli.main([])
        output = buf.getvalue()
        self.assertIn("Usage:", output)
        self.assertEqual(code, 0)

    def test_help_argument_shows_usage(self):
        """GIVEN the --help argument
        WHEN main is called
        THEN it should print usage and exit with code 0"""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli.main(["--help"])
        output = buf.getvalue()
        self.assertIn("Usage:", output)
        self.assertEqual(code, 0)

    def test_unknown_argument_returns_error(self):
        """GIVEN an unknown argument
        WHEN main is called
        THEN it should return exit code 1"""
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = cli.main(["--unknown"])
        output = buf.getvalue()
        self.assertIn("Usage:", output)
        self.assertEqual(code, 1)

    def test_scan_env_with_variables(self):
        """GIVEN environment variables for postgres
        WHEN scan_env is called
        THEN it should print the found variables"""
        env = {"PGHOST": "localhost", "PGPORT": "5432"}
        buf = io.StringIO()
        with patch.dict(os.environ, env, clear=True):
            with redirect_stdout(buf):
                cli.scan_env()
        output = buf.getvalue()
        self.assertIn("PGHOST=localhost", output)
        self.assertIn("PGPORT=5432", output)

    def test_scan_env_without_variables(self):
        """GIVEN no postgres environment variables
        WHEN scan_env is called
        THEN it should report nothing found"""
        buf = io.StringIO()
        with patch.dict(os.environ, {}, clear=True):
            with redirect_stdout(buf):
                cli.scan_env()
        output = buf.getvalue()
        self.assertIn("No postgres connection info found.", output)

    def test_history_file_written(self):
        """GIVEN a call to main
        WHEN it is executed
        THEN the invocation should be appended to the history file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            history = Path(tmpdir) / ".codextest_history"
            with patch.object(cli, "HISTORY_FILE", history):
                cli.main(["--test"])
            self.assertTrue(history.exists())
            content = history.read_text().strip()
            self.assertEqual(content, "--test")


if __name__ == "__main__":
    unittest.main()
