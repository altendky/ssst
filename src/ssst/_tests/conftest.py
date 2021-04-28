import functools
import pathlib
import typing

import attr
import click.testing
import pymodbus.client.asynchronous.tcp
import pymodbus.client.asynchronous.schedulers
import pytest
import _pytest.fixtures
import trio


pytest_plugins = "pytester"


# TODO: consider pytest-click


@pytest.fixture(name="frozen_executable", scope="session")
def frozen_executable_fixture(
    request: _pytest.fixtures.SubRequest,
) -> typing.Optional[pathlib.Path]:
    """If a test or fixture depends on this one but only conditionally makes use of
    it then it should consider the rules set out below in the _maybe_skip_not_frozen
    fixture.
    """
    maybe_frozen_executable_string = request.config.getoption("--frozen-executable")

    if maybe_frozen_executable_string is None:
        return None

    return pathlib.Path(maybe_frozen_executable_string)


@pytest.fixture(name="_maybe_skip_not_frozen", autouse=True, scope="function")
def _maybe_skip_not_frozen_fixture(request: _pytest.fixtures.SubRequest):
    """If a frozen executable has been specified, this will skip all tests that
    don't at least maybe use the frozen executable fixture.  Any fixtures or
    tests that depend on the frozen executable fixture but only use it
    conditionally are responsible for skipping their own non-using cases.
    """

    frozen_executable_specified = (
        request.config.getoption("--frozen-executable") is not None
    )
    uses_frozen_executable = "frozen_executable" in request.fixturenames

    if frozen_executable_specified and not uses_frozen_executable:
        pytest.skip("Frozen executable specified, skipping non-frozen tests")


@pytest.fixture(name="cli_runner")
def cli_runner_fixture() -> typing.Iterator[click.testing.CliRunner]:
    cli_runner = click.testing.CliRunner()
    with cli_runner.isolated_filesystem():
        yield cli_runner
