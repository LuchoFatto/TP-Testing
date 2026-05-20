from app.services.event_service import EventService


def test_list_events_active_only(monkeypatch):
    sample_events = [
        {"id": 1, "name": "A", "active": True, "deleted": False},
        {"id": 2, "name": "B", "active": False, "deleted": False},
        {"id": 3, "name": "C", "active": True, "deleted": True},
    ]

    monkeypatch.setattr(
        "app.services.event_service.event_repository.read_all",
        lambda: sample_events
    )

    events = EventService.list_events(active_only=True)
    assert len(events) == 1
    assert events[0]["id"] == 1