#!/usr/bin/env pytest -vs
"""Tests for opc."""

import sys
from unittest.mock import patch

import pytest

import opc


def test_version(capsys):
    """Verify that version string sent to stdout, and agrees with the module."""
    with pytest.raises(SystemExit):
        with patch.object(sys, "argv", ["bogus", "--version"]):
            opc.multi_opc.main()
    captured = capsys.readouterr()
    assert (
        captured.out == f"{opc.__version__}\n"
    ), "standard output by '--version' should agree with module.__version__"
