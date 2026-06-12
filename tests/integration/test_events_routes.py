from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def headers(username: str) -> dict:
    return {"Authorization": f"Bearer token-{username}"}

def test_list_events_active_only_default():
    response = client.get("/events")
    assert response.status_code == 200
    ids = [e["id"] for e in response.json()]
    assert 3 not in ids


def test_list_events_active_only_false_includes_inactive():
    response = client.get("/events", params={"active_only": False})
    assert response.status_code == 200
    ids = [e["id"] for e in response.json()]
    assert 3 in ids


def test_get_event_found():
    response = client.get("/events/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_event_not_found():
    response = client.get("/events/9999")
    assert response.status_code == 404


def test_create_event_as_organizer_ok():
    response = client.post(
        "/events",
        json={"name": "Nuevo", "date": "2026-09-01", "capacity": 100, "price": 25.0},
        headers=headers("organizer1"),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Nuevo"
    assert body["owner_username"] == "organizer1"


def test_create_event_forbidden_for_customer():
    response = client.post(
        "/events",
        json={"name": "X", "date": "2026-09-01", "capacity": 10, "price": 5.0},
        headers=headers("customer1"),
    )
    assert response.status_code == 403


def test_create_event_requires_auth():
    response = client.post(
        "/events",
        json={"name": "X", "date": "2026-09-01", "capacity": 10, "price": 5.0},
    )
    assert response.status_code == 401


def test_create_event_invalid_payload():
    response = client.post(
        "/events",
        json={"name": "X", "date": "2026-09-01", "capacity": 0, "price": 5.0},
        headers=headers("organizer1"),
    )
    assert response.status_code == 422

def _valid_update(**overrides):
    payload = {
        "name": "Rock Fest",
        "date": "2026-01-01",
        "capacity": 500,
        "price": 80.0,
        "active": True,
    }
    payload.update(overrides)
    return payload


def test_update_event_admin_ok():
    response = client.put("/events/1", json=_valid_update(), headers=headers("admin1"))
    assert response.status_code == 200
    assert response.json()["capacity"] == 500


def test_update_event_not_found():
    response = client.put("/events/9999", json=_valid_update(), headers=headers("admin1"))
    assert response.status_code == 404


def test_update_event_forbidden_for_other_organizer():
    # evento 1 pertenece a organizer1
    response = client.put("/events/1", json=_valid_update(), headers=headers("organizer2"))
    assert response.status_code == 403


def test_update_event_capacity_below_sold_returns_400():
    # evento 1 tiene 2 tickets vendidos (orden activa qty=2)
    response = client.put(
        "/events/1", json=_valid_update(capacity=1), headers=headers("admin1")
    )
    assert response.status_code == 400


# --------------------------------------------------------------------------- #
# PATCH /events/{id}/capacity
# --------------------------------------------------------------------------- #
def test_update_capacity_ok():
    response = client.patch(
        "/events/1/capacity", json={"capacity": 999}, headers=headers("organizer1")
    )
    assert response.status_code == 200
    assert response.json()["capacity"] == 999


def test_update_capacity_not_found():
    response = client.patch(
        "/events/9999/capacity", json={"capacity": 10}, headers=headers("admin1")
    )
    assert response.status_code == 404


def test_update_capacity_below_sold_returns_400():
    response = client.patch(
        "/events/1/capacity", json={"capacity": 1}, headers=headers("admin1")
    )
    assert response.status_code == 400


def test_update_capacity_forbidden():
    response = client.patch(
        "/events/1/capacity", json={"capacity": 50}, headers=headers("organizer2")
    )
    assert response.status_code == 403


def test_deactivate_event_ok():
    response = client.patch("/events/1/deactivate", headers=headers("organizer1"))
    assert response.status_code == 200
    assert response.json()["active"] is False


def test_deactivate_event_not_found():
    response = client.patch("/events/9999/deactivate", headers=headers("admin1"))
    assert response.status_code == 404


def test_deactivate_event_forbidden():
    response = client.patch("/events/1/deactivate", headers=headers("organizer2"))
    assert response.status_code == 403


def test_delete_event_admin_ok():
    response = client.delete("/events/2", headers=headers("admin1"))
    assert response.status_code == 200
    assert response.json()["deleted"] is True


def test_delete_event_owner_with_orders_returns_409():
    # evento 1 (owner organizer1) tiene una orden registrada
    response = client.delete("/events/1", headers=headers("organizer1"))
    assert response.status_code == 409


def test_delete_event_not_found():
    response = client.delete("/events/9999", headers=headers("admin1"))
    assert response.status_code == 404


def test_delete_event_forbidden():
    response = client.delete("/events/1", headers=headers("organizer2"))
    assert response.status_code == 403
