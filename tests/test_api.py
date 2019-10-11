# -*- coding: utf-8 -*-
"""Tests for the `api` module."""

from unittest.mock import Mock, patch

from botocore import exceptions

from statikos import utils
from statikos.api import CloudFormation
from statikos.exceptions import InvalidTemplate

from .base import AWSBaseTestCase


class AWSTestCase(AWSBaseTestCase):
    def setUp(self):
        super(AWSTestCase, self).setUp()

    def test_get_session(self):
        self.aws._get_session()
        self.mock_session.assert_called_with(region_name='region')

    def test_get_client(self):
        self.aws._get_client()
        self.session.client.assert_called_with(None, use_ssl=True)


class CloudFormationTestCase(AWSBaseTestCase):
    def setUp(self):
        super(CloudFormationTestCase, self).setUp()
        self.cfn = CloudFormation()
        self.cfn.client = Mock()

        self.mock_read_file = patch.object(utils, 'read_file').start()
        self.mock_read_file.return_value = '{}'

        self.patch_is_valid_template = patch.object(
            CloudFormation, 'is_valid_template'
        )
        self.mock_is_valid_template = self.patch_is_valid_template.start()

        self.patch_stack_exists = patch.object(CloudFormation, 'stack_exists')
        self.mock_stack_exists = self.patch_stack_exists.start()

        self.patch_create_stack = patch.object(CloudFormation, 'create_stack')
        self.mock_create_stack = self.patch_create_stack.start()

        self.patch_update_stack = patch.object(CloudFormation, 'update_stack')
        self.mock_update_stack = self.patch_update_stack.start()

        self.patch_delete_stack = patch.object(CloudFormation, 'delete_stack')
        self.mock_delete_stack = self.patch_delete_stack.start()

        self.patch_validate_template = patch.object(
            CloudFormation, 'validate_template'
        )
        self.mock_validate_template = self.patch_validate_template.start()

    def test_deploy_stack_does_not_exist(self):
        parameter_overrides = [
            'ParameterKey1=ParameterValue1', 'ParameterKey2=ParameterValue2'
        ]
        self.mock_stack_exists.return_value = False
        self.cfn.deploy('stack_name', 'path/to/template', parameter_overrides)
        self.mock_stack_exists.assert_called_once_with('stack_name')
        self.mock_create_stack.assert_called_with(
            stack_name='stack_name',
            template_body='{}',
            parameters=[{
                'ParameterKey': 'ParameterKey1',
                'ParameterValue': 'ParameterValue1',
            }, {
                'ParameterKey': 'ParameterKey2',
                'ParameterValue': 'ParameterValue2',
            }]
        )

    def test_deploy_stack_exists(self):
        parameter_overrides = [
            'ParameterKey1=ParameterValue1', 'ParameterKey2=ParameterValue2'
        ]
        self.cfn.deploy('stack_name', 'path/to/template', parameter_overrides)
        self.mock_update_stack.assert_called_with(
            stack_name='stack_name',
            template_body='{}',
            parameters=[{
                'ParameterKey': 'ParameterKey1',
                'ParameterValue': 'ParameterValue1',
            }, {
                'ParameterKey': 'ParameterKey2',
                'ParameterValue': 'ParameterValue2',
            }]
        )

    def test_deploy_stack_invalid_template(self):
        self.mock_is_valid_template.return_value = False
        with self.assertRaises(InvalidTemplate):
            self.cfn.deploy('stack_name', 'path/to/template', [])

    def test_is_valid_template_true(self):
        self.patch_is_valid_template.stop()
        self.assertTrue(self.cfn.is_valid_template('{}'))

    def test_is_valid_template_false(self):
        self.patch_is_valid_template.stop()
        self.cfn.validate_template.side_effect = \
            exceptions.ValidationError(value='', param='', type_name='')
        self.assertFalse(self.cfn.is_valid_template(''))

    def test_stack_exists_true(self):
        self.patch_stack_exists.stop()
        self.assertTrue(self.cfn.stack_exists('stack_name'))

    def test_stack_exists_false(self):
        self.patch_stack_exists.stop()
        self.cfn.client.describe_stacks.side_effect = \
            exceptions.ClientError(
                error_response={'Error': {
                    'Code': 'Code',
                    'Message': 'Message'
                }},
                operation_name='Operation'
            )
        self.assertFalse(self.cfn.stack_exists('stack_name'))

    def test_create_stack(self):
        self.patch_create_stack.stop()
        self.cfn.create_stack('stack_name', '{}', [])
        self.cfn.client.create_stack.assert_called_with(
            StackName='stack_name', TemplateBody='{}', Parameters=[]
        )

    def test_update_stack(self):
        self.patch_update_stack.stop()
        self.cfn.update_stack('stack_name', '{}', [])
        self.cfn.client.update_stack.assert_called_with(
            StackName='stack_name', TemplateBody='{}', Parameters=[]
        )

    def test_delete_stack(self):
        self.patch_delete_stack.stop()
        self.cfn.delete_stack('stack_name')
        self.cfn.client.delete_stack.assert_called_with(StackName='stack_name')

    def test_validate_template(self):
        self.patch_validate_template.stop()
        self.cfn.validate_template('{}')
        self.cfn.client.validate_template.assert_called_with(
            TemplateBody='{}',
        )
