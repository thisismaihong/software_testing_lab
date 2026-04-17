from eapp.test.test_base import test_app, test_client

def test_add_to_cart_success(test_client):
    test_client.post("/api/carts", json={
        "id":1,
        "name":"iPhone",
        "price":50
    })
    res=test_client.post("/api/carts", json={
        "id":1,
        "name":"iPhone",
        "price":50
    })

    data=res.get_json()
    assert data["total_quantity"]==2
    assert data["total_amount"]==100

def test_add_cart_increase(test_client):
    test_client.post("api/carts",json={
        "id": 1,
        "name": "iPhone",
        "price": 50
    })
    test_client.post("api/carts", json={
        "id": 1,
        "name": "iPhone",
        "price": 50
    })
    res=test_client.post("api/carts", json={
        "id": 2,
        "name": "Galaxy",
        "price": 200
    })

    data=res.get_json()

    assert data["total_quantity"]==3
    assert data["total_amount"] == 300

    with test_client.session_transaction() as session:
        assert "cart" in session
        assert len(session["cart"])==2
        assert session["cart"]["1"]["quantity"]==2


def test_existing_item(test_client):
    with test_client.session_transaction() as session:
        session["cart"]={
            "1":{
                "id":"1",
                "name":"old",
                "price":900,
                "quantity": 2
            }
        }

    res=test_client.post("/api/carts",json={
        "id":1,
        "name": "new",
        "price": 100
    })

    data=res.get_json()
    assert data["total_quantity"]==3

    with test_client.session_transaction() as session:
        assert session["cart"]["1"]["quantity"]==3


def test_update_cart(test_client):
    with test_client.session_transaction() as session:
        session["cart"] = {
            "1": {
                "id": 1,
                "name": "iphone",
                "price": 900,
                "quantity": 2
            }
        }

    res = test_client.put("/api/carts/1", json={
        "quantity": 5
    })

    data = res.get_json()
    assert data["total_quantity"] == 5
    assert data["total_amount"]==4500

    with test_client.session_transaction() as session:
        assert len(session["cart"])==1


def test_delete_cart(test_client):
    with test_client.session_transaction() as session:
        session["cart"]={
            "1":{
                "id":"1",
                "name":"ip",
                "price":1200,
                "quantity": 2
            },
            "2": {
                "id": "2",
                "name": "samsung",
                "price": 1000,
                "quantity": 1
            }
        }

    res=test_client.delete("/api/carts/2")
    data=res.get_json()

    assert data["total_quantity"] == 2
    assert data["total_amount"] == 2400

    with test_client.session_transaction() as session:
        assert "2" not in session["cart"]



        
