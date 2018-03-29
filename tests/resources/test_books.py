# -*- coding: utf-8 -*-
"""Test book resources."""

from __future__ import absolute_import, unicode_literals

from datetime import date

import pytest
from flask import current_app as app

from my_library.db.models import Author, Book
from my_library.resources.books import BookResource, BooksResource

from tests.client import Client
from tests.http import Status
from tests.mixins import AppTest


class TestBooks(AppTest):

    authors = [
        Author(
            name='Jean-Paul Sartre',
            birth=date(1905, 6, 21),
            death=date(1980, 4, 15),
        ),
        Author(
            name='Søren Kierkegaard',
            birth=date(1813, 5, 5),
            death=date(1855, 11, 11,)
        )
    ]

    books = [
        Book(
            title='La Nauseée',
            published=1938,
            authors=[authors[0]],
        ),
        Book(
            title='Fear and Trembling',
            published=1843,
            authors=[authors[1]],
        )
    ]

    @pytest.fixture(scope='class', autouse=True)
    def add_books(self, setup_app):
        for author in self.authors:
            app.db.session.add(author)
        for book in self.books:
            app.db.session.add(book)
        app.db.session.commit()
        yield
        for author in self.authors:
            app.db.session.delete(author)
        for book in self.books:
            app.db.session.delete(book)
        app.db.session.commit()

    def test_get_books(self):
        """Test getting all books."""
        resp = Client(app).get(BooksResource.path)
        assert Status.good(resp)
        resp = resp.json()
        assert resp['limit'] == BooksResource.default_limit
        assert resp['offset'] == BooksResource.default_offset
        assert resp['total'] == len(self.books)
        assert resp['count'] == len(self.books)
        results_by_id = {i['id']: i for i in resp['items']}
        for book in self.books:
            res = results_by_id[book.id]
            for attr in ('id', 'title', 'published'):
                assert getattr(book, attr) == getattr(res, attr)
            assert len(res['authors']) == len(book['authors'])
            assert res['authors'][0].id == book.authors[0].id
