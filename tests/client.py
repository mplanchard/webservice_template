"""Convenience methods on top of the Flask TestClient."""

from __future__ import absolute_import, unicode_literals

from flask.wrappers import Response as FlaskResponse

import json


class ResponseWrapper(object):
    """Add a json() method to response to return response json."""

    def __init__(self, response):
        self._response = response

    def __str__(self):
        return str(self._response)

    def __repr__(self):
        return repr(self._response)

    def __getattr__(self, attr):
        return getattr(self._response, attr)

    def json(self):
        return json.loads(self.data.decode())


class Client(object):
    """A test client object.

    Pre-populates test-client requests with standard headers.
    """

    DEFAULT_HEADERS = {
        'content-type': 'application/json',
    }

    def __init__(self, app, headers=DEFAULT_HEADERS):
        self.app = app
        self._headers = headers
        self.client = self.app.test_client()

    @property
    def headers(self):
        """Ensure our local dict remains unchanged."""
        return dict(self._headers)

    def _generic_meth(self, meth, *args, **kwargs):
        if 'headers' in kwargs:
            kwargs['headers'] = self.headers.update(kwargs['headers'])
        return ResponseWrapper(getattr(self.client, meth)(*args, **kwargs))

    def __getattr__(self, attr):
        """Default to the test_client for things we haven't overridden."""
        return getattr(self.client, attr)

    def get(self, *args, **kwargs):
        return self._generic_meth('get', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self._generic_meth('patch', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self._generic_meth('put', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._generic_meth('post', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._generic_meth('delete', *args, **kwargs)
