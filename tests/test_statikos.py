# -*- coding: utf-8 -*-
"""Tests for the `statikos` module."""

from unittest.mock import Mock, patch

from statikos import statikos, utils
from statikos.exceptions import ConfigNotFound
from statikos.statikos import Statikos

from .base import BaseTestCase


class StatikosTestCase(BaseTestCase):
    def setUp(self):
        super(StatikosTestCase, self).setUp()
        self.mock_cfn = Mock()
        self.mock_cloudformation = patch.object(statikos,
                                                'CloudFormation').start()
        self.mock_cloudformation.return_value = self.mock_cfn

        self.mock_touch = patch.object(utils, 'touch').start()
        self.mock_mkdir = patch.object(utils, 'mkdir').start()

        self.mock_write_json_file = patch.object(utils,
                                                 'write_json_file').start()

        self.mock_read_file = patch.object(utils, 'read_file').start()
        self.mock_read_file.return_value = {}

        self.mock_write_file = patch.object(utils, 'write_file').start()

        self.mock_read_yaml_file = patch.object(utils,
                                                'read_yaml_file').start()
        self.mock_read_yaml_file.return_value = {}

        self.mock_template = Mock()
        self.mock_create_template = patch.object(statikos,
                                                 'create_template').start()
        self.mock_create_template.return_value = self.mock_template

        self.patch_get_config = patch.object(Statikos, '_get_config')
        self.mock_get_config = self.patch_get_config.start()
        self.mock_get_config.return_value = {}

        self.patch_configure = patch.object(Statikos, '_configure')
        self.mock_configure = self.patch_configure.start()

        self.patch_create = patch.object(Statikos, 'create')
        self.mock_create = self.patch_create.start()

    def test_init(self):
        kwargs = {'a': 1, 'b': 2, 'c': 3}
        s = Statikos(**kwargs)
        self.assertEqual(1, s.a)
        self.assertEqual(2, s.b)
        self.assertEqual(3, s.c)
        self.mock_cloudformation.assert_called_once()
        self.mock_get_config.assert_called_once()

    def test_get_config(self):
        s = Statikos()
        self.patch_get_config.stop()
        result = s._get_config()
        self.mock_read_yaml_file.assert_called_with('statikos.yml')
        self.assertEqual({}, result)

    def test_get_config_file_not_found(self):
        s = Statikos()
        self.patch_get_config.stop()
        self.mock_read_yaml_file.side_effect = FileNotFoundError
        with self.assertRaises(ConfigNotFound):
            s._get_config()
        self.mock_read_yaml_file.assert_called_with('statikos.yml')

    def test_configure(self):
        s = Statikos()
        self.patch_configure.stop()
        s._configure()
        self.mock_mkdir.assert_called_once_with('.statikos')
        self.mock_touch.assert_called_once_with(
            ('.statikos/cloudformation.json')
        )

    def test_create(self):
        self.patch_create.stop()
        self.mock_get_config.return_value = {'a': 1, 'b': 2, 'c': 3}
        s = Statikos()
        s.create()
        self.mock_configure.assert_called_once()
        self.mock_create_template.assert_called_with(
            parameters={
                'a': 1,
                'b': 2,
                'c': 3
            }
        )
        self.mock_write_json_file.assert_called_once_with(
            self.mock_template.to_dict(), '.statikos/cloudformation.json'
        )

    def test_deploy(self):
        self.mock_get_config.return_value = {'stack_name': 'stack_name'}
        s = Statikos()
        s.deploy()
        self.mock_create.assert_called_once()
        self.mock_cfn.deploy.assert_called_once_with(
            stack_name='stack_name',
            template_file='.statikos/cloudformation.json'
        )

    def test_remove(self):
        self.mock_get_config.return_value = {'stack_name': 'stack_name'}
        s = Statikos()
        s.remove()
        self.mock_cfn.delete.assert_called_once_with(stack_name='stack_name')
