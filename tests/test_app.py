"""Test basic app functionality."""

import pytest

from my_library.app import create_app

from .mixins import SessionFreshDB


class TestApp(SessionFreshDB):

    def test_instantiation_without_errors(self):
        create_app()


