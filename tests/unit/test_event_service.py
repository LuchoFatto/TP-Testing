import pytest

from app.services.event_service import EventService


ADMIN = {"role": "admin", "username": "admin1"}
OWNER = {"role": "customer", "username": "owner1"}
OTHER = {"role": "customer", "username": "other1"}


def make_event(**overrides):
    base = {
        "id": 1,
        "name": "A",
        "date": "2026-01-01",
        "capacity": 100,
        "price": 50.0,
        "active": True,
        "deleted": False,
        "owner_username": "owner1",
    }
    base.update(overrides)
    return base


@pytest.fixture
def repo(monkeypatch):
    """Mockea el repositorio en memoria y captura lo que se escribe."""
    store = {"events": [], "written": None}

    monkeypatch.setattr(
        "app.services.event_service.event_repository.read_all",
        lambda: [dict(e) for e in store["events"]],
    )

    def fake_write(data):
        store["written"] = data

    monkeypatch.setattr(
        "app.services.event_service.event_repository.write_all", fake_write
    )
    return store


@pytest.fixture
def no_sold(monkeypatch):
    monkeypatch.setattr(
        "app.services.order_service.OrderService.sold_tickets_for_event",
        lambda event_id: 0,
    )

def test_list_events_active_only(repo):
    repo["events"] = [
        make_event(id=1, active=True, deleted=False),
        make_event(id=2, active=False, deleted=False),
        make_event(id=3, active=True, deleted=True),
    ]
    events = EventService.list_events(active_only=True)
    assert len(events) == 1
    assert events[0]["id"] == 1


def test_list_events_includes_inactive_when_not_active_only(repo):
    repo["events"] = [
        make_event(id=1, active=True, deleted=False),
        make_event(id=2, active=False, deleted=False),
        make_event(id=3, active=True, deleted=True),
    ]
    events = EventService.list_events(active_only=False)
    # incluye activos e inactivos, pero nunca eliminados
    assert {e["id"] for e in events} == {1, 2}


def test_list_all_events_returns_everything(repo):
    repo["events"] = [
        make_event(id=1, deleted=False),
        make_event(id=2, deleted=True),
    ]
    events = EventService.list_all_events()
    assert len(events) == 2


def test_get_event_found(repo):
    repo["events"] = [make_event(id=7)]
    assert EventService.get_event(7)["id"] == 7


def test_get_event_not_found(repo):
    repo["events"] = [make_event(id=1)]
    assert EventService.get_event(999) is None

def test_create_event_first_id_is_one(repo):
    repo["events"] = []
    event = EventService.create_event("Show", "2026-05-01", 200, 99.0, "owner1")
    assert event["id"] == 1
    assert event["active"] is True
    assert event["deleted"] is False
    assert event["owner_username"] == "owner1"
    assert repo["written"][-1]["id"] == 1


def test_create_event_next_id_is_max_plus_one(repo):
    repo["events"] = [make_event(id=4), make_event(id=9)]
    event = EventService.create_event("Show", "2026-05-01", 50, 10.0, "owner1")
    assert event["id"] == 10


def test_update_event_ok(repo, no_sold):
    repo["events"] = [make_event(id=1, capacity=100)]
    updated = EventService.update_event(1, {"capacity": 150}, ADMIN)
    assert updated["capacity"] == 150
    assert repo["written"][0]["capacity"] == 150


def test_update_event_owner_can_update(repo, no_sold):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    updated = EventService.update_event(1, {"name": "Nuevo", "capacity": 100}, OWNER)
    assert updated["name"] == "Nuevo"


def test_update_event_not_found_raises(repo):
    repo["events"] = []
    with pytest.raises(ValueError, match="Event not found"):
        EventService.update_event(1, {"capacity": 10}, ADMIN)


def test_update_event_deleted_raises(repo):
    repo["events"] = [make_event(id=1, deleted=True)]
    with pytest.raises(ValueError, match="Event not found"):
        EventService.update_event(1, {"capacity": 10}, ADMIN)


def test_update_event_permission_denied(repo):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    with pytest.raises(PermissionError):
        EventService.update_event(1, {"capacity": 10}, OTHER)


def test_update_event_capacity_below_sold_raises(repo, monkeypatch):
    repo["events"] = [make_event(id=1, capacity=100)]
    monkeypatch.setattr(
        "app.services.order_service.OrderService.sold_tickets_for_event",
        lambda event_id: 30,
    )
    with pytest.raises(ValueError, match="Capacity cannot be lower"):
        EventService.update_event(1, {"capacity": 10}, ADMIN)

def test_deactivate_event_ok(repo):
    repo["events"] = [make_event(id=1, active=True)]
    result = EventService.deactivate_event(1, ADMIN)
    assert result["active"] is False
    assert repo["written"][0]["active"] is False


def test_deactivate_event_not_found_raises(repo):
    repo["events"] = []
    with pytest.raises(ValueError, match="Event not found"):
        EventService.deactivate_event(1, ADMIN)


def test_deactivate_event_permission_denied(repo):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    with pytest.raises(PermissionError):
        EventService.deactivate_event(1, OTHER)

def test_delete_event_admin_ok(repo):
    repo["events"] = [make_event(id=1)]
    result = EventService.delete_event(1, ADMIN)
    assert result["deleted"] is True
    assert result["active"] is False


def test_delete_event_owner_without_orders_ok(repo, monkeypatch):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    monkeypatch.setattr(
        "app.services.order_service.OrderService.event_has_any_orders",
        lambda event_id: False,
    )
    result = EventService.delete_event(1, OWNER)
    assert result["deleted"] is True


def test_delete_event_owner_with_orders_raises(repo, monkeypatch):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    monkeypatch.setattr(
        "app.services.order_service.OrderService.event_has_any_orders",
        lambda event_id: True,
    )
    with pytest.raises(ValueError, match="registered orders"):
        EventService.delete_event(1, OWNER)


def test_delete_event_not_found_raises(repo):
    repo["events"] = []
    with pytest.raises(ValueError, match="Event not found"):
        EventService.delete_event(1, ADMIN)


def test_delete_event_permission_denied(repo):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    with pytest.raises(PermissionError):
        EventService.delete_event(1, OTHER)

def test_update_capacity_ok(repo, no_sold):
    repo["events"] = [make_event(id=1, capacity=100)]
    result = EventService.update_capacity(1, 250, ADMIN)
    assert result["capacity"] == 250
    assert repo["written"][0]["capacity"] == 250


def test_update_capacity_not_found_raises(repo):
    repo["events"] = []
    with pytest.raises(ValueError, match="Event not found"):
        EventService.update_capacity(1, 250, ADMIN)


def test_update_capacity_permission_denied(repo):
    repo["events"] = [make_event(id=1, owner_username="owner1")]
    with pytest.raises(PermissionError):
        EventService.update_capacity(1, 250, OTHER)


def test_update_capacity_below_sold_raises(repo, monkeypatch):
    repo["events"] = [make_event(id=1, capacity=100)]
    monkeypatch.setattr(
        "app.services.order_service.OrderService.sold_tickets_for_event",
        lambda event_id: 80,
    )
    with pytest.raises(ValueError, match="Capacity cannot be lower"):
        EventService.update_capacity(1, 50, ADMIN)