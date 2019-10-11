# -*- coding: utf-8 -*-
"""Utils module."""

import json
import os
from pathlib import Path

import yaml


def touch(filename: str) -> None:
    """
    Touch a file.

    *From the BSD General Commands Manual*:
    The touch utility sets the modification and access times of files. If any
    file does not exist, it is created with default permissions.

    :type filename: str
    :param filename: name of file

    :rtype: None
    :return: None
    """
    Path(filename).touch()


def mkdir(path: str) -> None:
    """
    Make a directory.

    *From the BSD General Commands Manual*:
    The mkdir utility creates the directories named as operands, in the order
    specified, using mode rwxrwxrwx (0777) as modified by the current umask(2).

    If the directory already exists, swallow the FileExistsError exception.

    :type path: str
    :param path: path to directory

    :rtype: None
    :return: None
    """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def read_file(filename: str) -> str:
    """
    Read a file.

    :type filename: str
    :param filename: name of file

    :rtype: str
    :return: str of contents
    """
    with open(filename, 'r') as f:
        return f.read()


def append_file(data: str, filename: str) -> None:
    """
    Append a file.

    :type data: str
    :param data: data to write
    :type filename: str
    :param filename: name of file

    :rtype: None
    :return: None
    """
    with open(filename, 'a') as f:
        f.write(data)


def write_file(data: str, filename: str) -> None:
    """
    Write a file.

    :type data: str
    :param data: data to write
    :type filename: str
    :param filename: name of file

    :rtype: None
    :return: None
    """
    with open(filename, 'w') as f:
        f.write(data)


def read_json_file(filename: str) -> dict:
    """
    Read a JSON file.

    :type filename: str
    :param filename: name of file

    :rtype: dict
    :return: dict of contents
    """
    with open(filename, 'r') as f:
        return json.load(f)


def write_json_file(data: dict, filename: str) -> None:
    """
    Write a JSON file.

    Example:

    {'a': 1, 'b': {'c': 3, 'd': 4}}

    {
      "a": 1,
      "b": {
        "c": 3,
        "d": 4
      }
    }

    :type data: dict
    :param data: data to write
    :type filename: str
    :param filename: name of file

    :rtype: None
    :return: None
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def read_yaml_file(filename: str) -> dict:
    """
    Read a YAML file.

    :type filename: str
    :param filename: name of file

    :rtype: dict
    :return: dict of contents
    """
    with open(filename, 'r') as f:
        return yaml.safe_load(f.read())


def write_yaml_file(data: dict, filename: str) -> None:
    """
    Write a YAML file.

    *From the PyYAML Documentation*:
    If you want collections to be always serialized in the block style, set the
    parameter default_flow_style of dump() to False.

    Example:

    {'a': 1, 'b': {'c': 3, 'd': 4}}

    a: 1
    b:
      c: 3
      d: 4

    :type data: dict
    :param data: data to write
    :type filename: str
    :param filename: name of file

    :rtype: None
    :return: None
    """
    with open(filename, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
