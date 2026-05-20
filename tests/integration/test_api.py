from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "Simple Testing Project" in response.text
    assert "Iniciar sesión" in response.text
    assert "Eventos disponibles" in response.text


def test_login_ok():
    response = client.post(
        "/auth/login",
        json={"username": "admin1", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "admin"
    assert data["token"] == "token-admin1"


def test_list_events_ok():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_customer_can_buy_and_cancel_order():
    login = client.post(
        "/auth/login",
        json={"username": "customer1", "password": "cust123"},
    )
    token = login.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    create = client.post(
        "/orders",
        json={"event_id": 1, "quantity": 1},
        headers=headers,
    )
    assert create.status_code == 200
    order_id = create.json()["id"]

    cancel = client.patch(f"/orders/{order_id}/cancel", headers=headers)
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"
