import pathlib
import shutil

import importlib_resources
import pytest
import _pytest.pytester
import qts

import ssst._tests
import ssst._utilities


def test_configure_qt_wrapper_raises(pytester: _pytest.pytester.Pytester) -> None:
    content = f"""
    import os
    import sys

    import pytest

    import ssst._utilities
    import ssst.exceptions


    if ssst._utilities.qt_api_variable_name in os.environ:
        os.environ.pop(ssst._utilities.qt_api_variable_name)


    def test():
        import qts
        qts.autoset_wrapper()

        with pytest.raises(ssst.exceptions.QtWrapperError, match="qts already configured"):
            ssst._utilities.configure_qt_wrapper(
                api=ssst._utilities.QtApis.PyQt5,
            )
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["api"],
    argvalues=[[api] for api in ssst._utilities.QtApis],
)
def test_configure_qt_wrapper_sets_requested_api(
    pytester: _pytest.pytester.Pytester,
    api: ssst._utilities.QtApis,
) -> None:
    content = f"""
    import os
    import sys

    import qts

    import ssst._utilities

    os.environ.pop(ssst._utilities.qt_api_variable_name)

    
    def test():
        assert qts.wrapper is None

        ssst._utilities.configure_qt_wrapper(
            api=ssst._utilities.QtApis({api.value!r}),
        )

        assert qts.wrapper.name == {api.name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=["api"],
    argvalues=[[api] for api in ssst._utilities.QtApis],
)
def test_configure_qt_wrapper_handles_env_var(
    pytester: _pytest.pytester.Pytester,
    api: ssst._utilities.QtApis,
) -> None:
    content = f"""
    import os
    import sys

    import qts

    import ssst._utilities

    os.environ[ssst._utilities.qt_api_variable_name] = {api.value!r}


    def test():
        assert qts.wrapper is None

        ssst._utilities.configure_qt_wrapper(api=42)

        assert qts.wrapper is not None
        assert qts.wrapper.name == {api.name!r}
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)


@pytest.fixture(name="tmp_path_with_ui")
def tmp_path_with_ui_fixture(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    directory_path = tmp_path_factory.mktemp(
        basename="tmp_path_with_ui_fixture", numbered=True
    )

    name = "example.ui"

    ui_source_file = importlib_resources.open_binary(package=ssst._tests, resource=name)
    ui_target_path = directory_path.joinpath(name)

    with ui_target_path.open("wb") as ui_target_file:
        shutil.copyfileobj(ui_source_file, ui_target_file)

    return directory_path


def test_compile_ui_defaults_to_no_output(
    capsys: pytest.CaptureFixture,
    tmp_path_with_ui: pathlib.Path,
) -> None:
    ssst._utilities.compile_ui(directory_path=[tmp_path_with_ui])

    captured = capsys.readouterr()
    assert captured.out == ""


def test_compile_ui_creates_expected_path(tmp_path_with_ui: pathlib.Path) -> None:
    [source_ui] = tmp_path_with_ui.iterdir()
    expected_ui_py = tmp_path_with_ui.joinpath(f"{source_ui.stem}_ui.py")

    assert set(tmp_path_with_ui.iterdir()) == {source_ui}

    ssst._utilities.compile_ui(directory_path=[tmp_path_with_ui])

    assert set(tmp_path_with_ui.iterdir()) == {source_ui, expected_ui_py}


def test_compile_paths_raises_if_qts_not_imported(
    pytester: _pytest.pytester.Pytester,
) -> None:
    content = f"""
    import pytest

    import ssst._utilities


    def test():
        with pytest.raises(
            ssst.QtWrapperError,
            match="qts is expected to be configured before calling this function.",
        ):
            ssst._utilities.compile_paths(ui_paths=[])
    """
    pytester.makepyfile(content)
    run_result = pytester.runpytest_subprocess()
    run_result.assert_outcomes(passed=1)
