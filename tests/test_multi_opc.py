#!/usr/bin/env pytest -vs
"""Tests for opc."""

import sys
from unittest.mock import patch

import pytest

from opc import multi_opc, __version__


def test_version(capsys):
    """Verify that version string sent to stdout, and agrees with the module."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            multi_opc.main()
    captured = capsys.readouterr()
    assert (
        captured.out == f"{__version__}\n"
    ), "standard output by '--version' should agree with module.__version__"
