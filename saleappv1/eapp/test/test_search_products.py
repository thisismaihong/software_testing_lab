import hashlib

import pytest
from flask import Flask
from eapp import db
from eapp.dao import load_products, add_user
from eapp.index import load_user
from eapp.models import Product, User, UserRole


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["PAGE_SIZE"] = 2
    db.init_app(app)
    return  app

@pytest.fixture
def test_app():
    app=create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_session(test_app):
    yield db.session

@pytest.fixture
def sample_product(test_session):
    p1=Product(name="Iphone 17", price="70", category_id=1)
    p2 = Product(name="Samsung galaxy ", price="20", category_id=1)
    p3 = Product(name="Ipad 7", price="50", category_id=2)
    p4 = Product(name="Iphone 13", price="15", category_id=2)
    test_session.add_all([p1,p2,p3,p4])
    test_session.commit()

    return [p1,p2,p3,p4]

def test_all(sample_product):
    actual_products=load_products()
    assert len(actual_products)==len(sample_product)

def test_kw(sample_product):
    actual_products=load_products(kw="Samsung")
    assert len(actual_products)==1
    assert all('Samsung' in p.name for p in actual_products)

def test_paging(sample_product):
    actual_products=load_products(page=1)
    assert len(actual_products)==2

    actual_products = load_products(page=3)
    assert len(actual_products) == 0


def test_cate_page(sample_product):
    actual_products=load_products(cate_id=1, page=1)
    assert len(actual_products)==2
    assert all(p.category_id==1 for p in actual_products)

    actual_products = load_products(cate_id=1, page=2)
    assert len(actual_products) == 0

def test_kw_page(sample_product):
    actual_products=load_products(kw="Iphone", page=1)
    assert len(actual_products)==2
    assert all("Iphone" in p.name for p in actual_products)


# @pytest.fixture
# def sample_user(test_session):
#     u = User(name='Admin', username='admin',
#              password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
#              user_role=UserRole.ADMIN)
#     db.session.add(u)
#     db.session.commit()
#     return u

def test_user():
    with pytest.raises(Exception) as e:
        add_user('Admin', 'admin', '123456', None)

    assert str(e.value) == 'Username đã tồn tại!'