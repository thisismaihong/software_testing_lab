from eapp.test.test_base import test_client, test_app

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

    # mocker.patch("eapp.dao.add_receipt")
    # res=test_client.post("/api/pay")
    #
    # data=res.get_json()
    # assert data["status"]==200
    # with test_client.session_transaction() as session:
    #     assert "cart" not in session

    #Truong hop that bai : Dùng side_effect giả lập lỗi
    mocker.patch("eapp.dao.add_receipt", side_effect=Exception("db error"))
    res = test_client.post("/api/pay")

    data = res.get_json()
    assert data["status"] == 400
    assert data["err_msg"]=="db error"
    with test_client.session_transaction() as session:
        assert "cart" in session
