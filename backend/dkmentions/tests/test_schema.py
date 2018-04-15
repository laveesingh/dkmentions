import pytest
from mixer.backend.django import mixer

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
