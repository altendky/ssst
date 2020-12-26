import typing

import click.testing
import pytest


pytest_plugins = "pytester"


# TODO: consider pytest-click


@pytest.fixture(name="cli_runner")
def cli_runner_fixture() -> typing.Iterator[click.testing.CliRunner]:
    cli_runner = click.testing.CliRunner()
    with cli_runner.isolated_filesystem():
        yield cli_runner
