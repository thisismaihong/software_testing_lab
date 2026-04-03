import hashlib

import pytest

from eapp.dao import add_user
from eapp.models import User
from eapp.test.test_base import test_app , test_session,mock_cloudinary


def test_register_success(test_session):
    add_user(name="abc", username="abcdefgh", password="abcd1234", avatar=None)
    u=User.query.filter(User.username.__eq__("abcdefgh")).first()

    assert u is not None
    assert u.name=="abc"
    assert u.password==str(hashlib.md5("abcd1234".encode("utf-8")).hexdigest())



@pytest.mark.parametrize("password", [
    '1','1'*8, 'a'*8, '1a1'*2
])
def test_invalid_password(password, test_session):
    with pytest.raises(ValueError):
        add_user(name="abc", username="abcdefgh", password=password, avatar=None)

def test_existing_username(test_session):
    add_user(name="abc", username="abcdefgh", password="abcd1234", avatar=None)
    with pytest.raises((ValueError)):
        add_user(name="abc", username="abcdefgh", password="abcd1234", avatar=None)


def test_avatar(test_session, mock_cloudinary):
    add_user(name="abc", username="abcdefgh", password="abcd1234", avatar="aaaaaa")
    u=User.query.filter(User.username.__eq__("abcdefgh")).first()

    assert u is not None
    assert u.name == "abc"
    assert u.password == str(hashlib.md5("abcd1234".encode("utf-8")).hexdigest())
    assert u.avatar=='https://fake-image.png'


