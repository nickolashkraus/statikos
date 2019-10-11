# -*- coding: utf-8 -*-
"""Tests for the `utils` module."""

from unittest.mock import Mock, mock_open, patch

from statikos import utils

from .base import BaseTestCase


class UtilsTestCase(BaseTestCase):
    def setUp(self):
        super(UtilsTestCase, self).setUp()
        self.mock_open = mock_open()
        self.mock_mkdir = patch('statikos.utils.os.mkdir').start()
        self.mock_json_dump = patch.object(utils.json, 'dump').start()
        self.mock_yaml_dump = patch.object(utils.yaml, 'dump').start()
        self.path = Mock()
        self.mock_path = patch('statikos.utils.Path').start()
        self.mock_path.return_value = self.path

    def test_touch(self):
        utils.touch('filename')
        self.path.touch.assert_called_once()

    def test_mkdir_directory_does_not_exist(self):
        utils.mkdir('path/to/directory')
        self.mock_mkdir.assert_called_once_with('path/to/directory')

    def test_mkdir_directory_does_exist(self):
        self.mock_mkdir.side_effect = FileExistsError
        utils.mkdir('path/to/directory')

    def test_read_file(self):
        read_data = 'data'
        self.mock_open = mock_open(read_data=read_data)
        with patch('builtins.open', self.mock_open):
            result = utils.read_file('filename')
        self.mock_open.assert_called_once_with('filename', 'r')
        self.assertEqual('data', result)

    def test_append_file(self):
        data = 'data'
        with patch('builtins.open', self.mock_open):
            utils.append_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'a')
        self.mock_open.return_value.write.assert_called_once_with('data')

    def test_write_file(self):
        data = 'data'
        with patch('builtins.open', self.mock_open):
            utils.write_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_open.return_value.write.assert_called_once_with('data')

    def test_read_json_file(self):
        read_data = '{"a": 1, "b": 2, "c": 3}'
        self.mock_open = mock_open(read_data=read_data)
        with patch('builtins.open', self.mock_open):
            result = utils.read_json_file('filename')
        self.mock_open.assert_called_once_with('filename', 'r')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_write_json_file(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        with patch('builtins.open', self.mock_open) as mock_file:
            utils.write_json_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_json_dump.assert_called_once_with(
            data, mock_file.return_value, indent=2
        )

    def test_read_yaml_file(self):
        read_data = \
            """
            a: 1
            b: 2
            c: 3
            """
        self.mock_open = mock_open(read_data=read_data)
        with patch('builtins.open', self.mock_open):
            result = utils.read_yaml_file('filename')
        self.mock_open.assert_called_once_with('filename', 'r')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_write_yaml_file(self):
        data = {'a': 1, 'b': 2, 'c': 3}
        with patch('builtins.open', self.mock_open) as mock_file:
            utils.write_yaml_file(data, 'filename')
        self.mock_open.assert_called_once_with('filename', 'w')
        self.mock_yaml_dump.assert_called_once_with(
            data, mock_file.return_value, default_flow_style=False
        )
