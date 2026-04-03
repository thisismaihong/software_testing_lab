from eapp.dao import load_products
from eapp.test.test_base import sample_product, test_session, test_app


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