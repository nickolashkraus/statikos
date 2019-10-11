# -*- coding: utf-8 -*-
"""Base test module."""

import unittest
from unittest.mock import Mock, patch

from statikos import api
from statikos.api import AWS


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.addCleanup(patch.stopall)


class AWSBaseTestCase(BaseTestCase):
    def setUp(self):
        super(AWSBaseTestCase, self).setUp()
        self.region = 'region'
        self.session = Mock()
        self.mock_session = patch.object(api.boto3, 'Session').start()
        self.mock_session.return_value = self.session
        self.aws = AWS(region=self.region)
