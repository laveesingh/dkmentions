import pytest
# from django.contrib.auth.models import AnonymousUser
# from django.test import RequestFactory
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
    query = schema.Query()
    res = query.resolve_all_posts(None, None, None)
    assert res.count() == 2, 'Should return all posts'


def test_resolve_first_post():
    msg = mixer.blend('dkmentions.FacebookPost')
    query = schema.Query()
    _id = to_global_id('FacebookPostType', msg.pk)
    res = query.resolve_first_post({'id': _id}, None, None)
    assert res == msg, 'Should return the first post'


# def test_create_facebook_post_mutation():
    # user = mixer.blend('auth.User')
    # mutation = schema.CreateFacebookPostMutation()
    # data = {
        # 'content': 'TestContent'
    # }
    # request = RequestFactory().get('/')
    # request.user = AnonymousUser()
    # response = mutation.mutate(None, data, request, None)
    # assert response.status == 403, 'Should return 403 if user is not logged in'

    # request.user = user
    # response = mutation.mutate(None, {}, req, None)
    # assert response.status == 400, 'Should return 400 if there are form errors'
    # assert 'content' in response.formErrors,\
            # 'Should have form error for content field'

    # response = mutation.mutate(None, data, request, None)
    # assert response.status == 200, 'Should return 200 if everything is fine'
    # assert response
