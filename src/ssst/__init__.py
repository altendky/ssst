"""Top-level package for SSST."""

from ssst.exceptions import (
    SsstError,
    InternalError,
    QtWrapperError,
    ReuseError,
    UnexpectedEmissionError,
)

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
