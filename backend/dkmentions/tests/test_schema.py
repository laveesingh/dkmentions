import pytest
from mixer.backend.django import mixer
from graphql_relay.node.node import to_global_id

from dkmentions import schema

pytestmark = pytest.mark.django_db


def test_facebookpost_type():
    instance = schema.FacebookPostType()
    assert instance, 'facebook post instance should be created'


def test_resolve_all_posts():
    mixer.blend('dkmentions.FacebookPost')
    mixer.blend('dkmentions.FacebookPost')
    q = schema.Query()
    res = q.resolve_all_posts(None, None, None)
    assert res.count() == 2, 'Should return all posts'


def test_resolve_first_post():
    msg = mixer.blend('dkmentions.FacebookPost')
    q = schema.Query()
    _id = to_global_id('FacebookPostType', msg.pk)
    res = q.resolve_first_post({'id': _id}, None, None)
    assert res == msg, 'Should return the first post'
