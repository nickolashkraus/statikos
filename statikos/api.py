# -*- coding: utf-8 -*-
"""AWS API module."""

import boto3
import botocore
from botocore import exceptions

from . import utils
from .exceptions import InvalidTemplate


class AWS:
    """
    Wrapper for the AWS SDK for Python.

    The AWS class provides a default configuration for a `boto3.Session` from
    which a low-level service client can be created.
    """
    SERVICE_NAME = None
    REGION = 'us-east-1'

    def __init__(self, region: str = None) -> None:
        """
        Create a new `AWS` object.

        :type region: str
        :param region: region associated with the client
            A client may only be associated with a single region.

        :rtype: None
        :return: None
        """
        self.region = region or self.REGION
        self.session = self._get_session()
        self.client = self._get_client()

    def _get_session(self) -> boto3.Session:
        """
        Create a session.

        :rtype: boto3.Session
        :return: a boto3 session instance
        """
        session_config = {'region_name': self.region}
        return boto3.Session(**session_config)

    def _get_client(self) -> botocore.client.BaseClient:
        """
        Create a low-level service client by name.

        :rtype: botocore.client.BaseClient
        :return: a botocore client instance
        """
        client_config = {
            'use_ssl': True,
        }
        return self.session.client(self.SERVICE_NAME, **client_config)


class CloudFormation(AWS):
    """
    Wrapper for a low-level client representing AWS CloudFormation.
    """
    SERVICE_NAME = 'cloudformation'

    def __init__(self, *args, **kwargs):
        """
        Create a new `CloudFormation` object.

        :rtype: None
        :return: None
        """
        super(CloudFormation, self).__init__(*args, **kwargs)

    def deploy(
        self,
        stack_name: str,
        template_file: str,
        parameter_overrides: list = []
    ) -> dict:
        """
        Deploy a CloudFormation stack.

        This is a high-level function that is meant to emulate the `deploy`
        command of the AWS CLI. This command does not have a corresponding
        method in the AWS SDK for Python.

        If you specify an existing stack, the command updates the stack. If you
        specify a new stack, the command creates it.

        Example `parameter_overrides`:

        [
          'ParameterKey1=ParameterValue1', 'ParameterKey2=ParameterValue2', ...
        ]

        :type stack_name: str
        :param stack_name: name of the stack
        :type template_file: str
        :param template_file: path to the CloudFormation template
        :type parameter_overrides: list
        :param parameter_overrides: a list of input parameters

        :rtype: None
        :return: None
        """
        template_body = str(utils.read_file(template_file))
        if not self.is_valid_template(template_body):
            raise InvalidTemplate
        parameters = []
        for x in parameter_overrides:
            parameters.append({
                'ParameterKey': x.split('=')[0],
                'ParameterValue': x.split('=')[1],
            })
        if not self.stack_exists(stack_name):
            self.create_stack(
                stack_name=stack_name,
                template_body=template_body,
                parameters=parameters
            )
        else:
            self.update_stack(
                stack_name=stack_name,
                template_body=template_body,
                parameters=parameters
            )

    def is_valid_template(self, template_body: str) -> bool:
        """
        Determine if a CloudFormation template is valid.

        This is a high-level function that checks the validity of a
        CloudFormation template.

        :type template_body: str
        :param template_body: body of the CloudFormation template

        :rtype: bool
        :return: whether the CloudFormation template is valid
        """
        try:
            self.validate_template(template_body=template_body)
        except exceptions.ValidationError:
            return False
        return True

    def stack_exists(self, stack_name: str) -> bool:
        """
        Determine if a CloudFormation stack exists.

        This is a high-level function that uses the DescribeStacks API endpoint
        to determine if the specified CloudFormation stack exists.

        :type stack_name: str
        :param stack_name: name of the stack

        :rtype: bool
        :return: whether the CloudFormation stack exists
        """
        try:
            self.client.describe_stacks(StackName=stack_name)
        except exceptions.ClientError:
            return False
        return True

    def create_stack(
        self, stack_name: str, template_body: str, parameters: list
    ) -> dict:
        """
        Create a CloudFormation stack as specified in the template.

        :type stack_name: str
        :param stack_name: name of the stack
        :type template_body: str
        :param template_body: body of the CloudFormation template
        :type parameters: list
        :param parameters: a list of input parameters for the CloudFormation
            stack

        Example `parameters`:

        [
          {
            'ParameterKey1': 'string',
            'ParameterValue1': 'string'
          },
          {
            'ParameterKey2': 'string',
            'ParameterValue2': 'string'
          }
        ]

        Returns:

        {
          'StackId': 'string'
        }

        :rtype: dict
        :return: a dict containing the response for the request
        """
        return self.client.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters
        )

    def update_stack(
        self, stack_name: str, template_body: str, parameters: list
    ) -> dict:
        """
        Update a CloudFormation stack as specified in the template.

        :type stack_name: str
        :param stack_name: name of the stack
        :type template_body: str
        :param template_body: body of the CloudFormation template
        :type parameters: dict
        :param parameters: a list of input parameters for the stack

        Example `parameters`:

        [
          {
            'ParameterKey1': 'string',
            'ParameterValue1': 'string'
          },
          {
            'ParameterKey2': 'string',
            'ParameterValue2': 'string'
          }
        ]

        Returns:

        {
          'StackId': 'string'
        }

        :rtype: dict
        :return: a dict containing the response for the request
        """
        return self.client.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters
        )

    def delete_stack(self, stack_name: str):
        """
        Delete a CloudFormation stack.

        :type stack_name: str
        :param stack_name: name of the stack

        :rtype: None
        :return: None
        """
        return self.client.delete_stack(StackName=stack_name)

    def validate_template(self, template_body: str):
        """
        Validate a specified CloudFormation template.

        :type template_body: str
        :param template_body: body of the CloudFormation template

        :rtype: dict
        :return: a dict containing the response for the request
        """
        return self.client.validate_template(TemplateBody=template_body, )
