"""Test basic app functionality."""


from my_library.app import create_app


class TestApp(object):

    def test_instantiation_without_errors(self):
        create_app()

