# -*- coding: utf-8 -*-
"""CLI module."""

import click

from .statikos import Statikos


@click.group(invoke_without_command=True)
@click.version_option(prog_name='Statikos', message='%(prog)s %(version)s')
@click.pass_context
def cli(ctx: click.core.Context) -> None:
    """
    A Python package for generating static websites using AWS CloudFormation.

    \f

    :type ctx: click.core.Context
    :param ctx: Click context object

    :rtype: None
    :return: None
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        ctx.exit(1)


@cli.command()
def create():
    """
    Create a Statikos service.

    \f

    :rtype: None
    :return: None
    """
    s = Statikos()
    s.create()


@cli.command()
def deploy():
    """
    Deploy a Statikos service.

    \f

    :rtype: None
    :return: None
    """
    s = Statikos()
    s.deploy()


@cli.command()
def remove():
    """
    Remove a Statikos service.

    :rtype: None
    :return: None
    """
    s = Statikos()
    s.remove()


if __name__ == '__main__':
    cli()
