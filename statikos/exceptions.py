# -*- coding: utf-8 -*-
"""Exceptions module."""


class StatikosException(Exception):
    """
    Base exception class for Statikos exceptions.
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Create a new `StatikosException` object.

        :rtype: None
        :return: None
        """
        if hasattr(self, 'msg'):
            self.msg = self.msg.format(**kwargs)
        else:
            self.msg = ''
        super(StatikosException, self).__init__(self.msg)


class ConfigNotFound(StatikosException):
    """
    Raised when the `statikos.yml` file could not be found.
    """
    msg = 'The `statikos.yml` file could not be found.'


class InvalidTemplate(StatikosException):
    """
    Raised when the CloudFormation template is invalid.
    """
    msg = 'The CloudFormation template is invalid.'
