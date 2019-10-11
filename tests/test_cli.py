# -*- coding: utf-8 -*-
"""Tests for the `cli` module."""

from unittest.mock import Mock, patch

from click.testing import CliRunner

from statikos.cli import cli

from .base import AWSBaseTestCase


class CliTestCase(AWSBaseTestCase):
    def setUp(self):
        super(CliTestCase, self).setUp()
        self.runner = CliRunner()
        self.statikos = Mock()
        self.mock_statikos = patch('statikos.cli.Statikos').start()
        self.mock_statikos.return_value = self.statikos

    def test_cli_version(self):
        result = self.runner.invoke(cli, ['--version'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertIn('Statikos', result.output)

    def test_cli_no_subcommand(self):
        result = self.runner.invoke(cli)
        self.assertIsInstance(SystemExit(1), type(result.exception))
        self.assertEqual(1, result.exit_code)
        self.assertIn('Usage', result.output)

    def test_cli_create(self):
        result = self.runner.invoke(cli, ['create'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.statikos.create.assert_called_once()

    def test_cli_deploy(self):
        result = self.runner.invoke(cli, ['deploy'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.statikos.deploy.assert_called_once()

    def test_cli_remove(self):
        result = self.runner.invoke(cli, ['remove'])
        self.assertIs(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.statikos.remove.assert_called_once()
