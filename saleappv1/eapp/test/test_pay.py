from unicodedata import category

from eapp.test.test_base import test_client, test_app, test_session
from eapp.models import User, Product, Receipt, ReceiptDetails

def test_pay_success(test_client, mocker):
    class FakeUser:
        is_authenticated=True
    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())

    with test_client.session_transaction() as session:
        session["cart"]={
            "1":{
                "id": "1",
                "name":"ip",
                "price":100,
                "quantity":2
            }
        }

    #Truong hop thanh cong

    mocker.patch("eapp.dao.add_receipt")
    res=test_client.post("/api/pay")

    data=res.get_json()
    assert data["status"]==200
    with test_client.session_transaction() as session:
        assert "cart" not in session

    #Truong hop that bai : Dùng side_effect giả lập lỗi

    # mocker.patch("eapp.dao.add_receipt", side_effect=Exception("db error"))
    # res = test_client.post("/api/pay")
    #
    # data = res.get_json()
    # assert data["status"] == 400
    # assert data["err_msg"]=="db error"
    # with test_client.session_transaction() as session:
    #     assert "cart" in session


def test_all(test_session, test_client, mocker):
    u=User(username="demo", password="123", name="admin")
    test_session.add(u)

    p1=Product(name="product1", price=12, category_id=1)
    p2=Product(name="product2", price=12, category_id=1)
    test_session.add(p1)
    test_session.add(p2)
    test_session.commit()

    test_client.post("/api/carts", json={
        "id":1,
        "name":"product1",
        "price": 12
    })
    test_client.post("/api/carts", json={
        "id": 1,
        "name": "product1",
        "price": 12
    })
    test_client.post("/api/carts", json={
        "id": 2,
        "name": "product2",
        "price": 12
    })

    class FakeUser:
        is_authenticated=True

    mocker.patch("flask_login.utils._get_user", return_value=FakeUser())
    mocker.patch("eapp.dao.current_user", new=u)

    res=test_client.post("/api/pay")

    data=res.get_json()
    assert data["status"]==200
    with test_client.session_transaction() as session:
        assert "cart" not in session

    r=Receipt.query.first()
    assert r is not None
    assert r.user_id==1
    assert ReceiptDetails.query.count()==2

