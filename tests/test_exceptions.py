# -*- coding: utf-8 -*-
"""Tests for the `exceptions` module."""

from statikos.exceptions import (
    ConfigNotFound, InvalidTemplate, StatikosException
)

from .base import BaseTestCase


class StatikosExceptionTestCase(BaseTestCase):
    def setUp(self):
        super(StatikosExceptionTestCase, self).setUp()

    def test_init(self):
        e = StatikosException()
        self.assertEqual('', e.msg)


class ConfigNotFoundTestCase(BaseTestCase):
    def setUp(self):
        super(ConfigNotFoundTestCase, self).setUp()

    def test_init(self):
        e = ConfigNotFound()
        self.assertEqual('The `statikos.yml` file could not be found.', e.msg)


class InvalidTemplateTestCase(BaseTestCase):
    def setUp(self):
        super(InvalidTemplateTestCase, self).setUp()

    def test_init(self):
        e = InvalidTemplate()
        self.assertEqual('The CloudFormation template is invalid.', e.msg)
