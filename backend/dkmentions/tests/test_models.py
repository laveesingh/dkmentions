import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

def test_facebook_post():
    obj = mixer.blend('dkmentions.FacebookPost')
    assert obj.pk > 0

