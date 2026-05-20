from app.services.order_service import OrderService


def test_sold_tickets_for_event_counts_only_active_orders(monkeypatch):
    monkeypatch.setattr(
        OrderService,
        "list_orders",
        staticmethod(lambda: [
            {"id": 1, "event_id": 1, "quantity": 2, "status": "active"},
            {"id": 2, "event_id": 1, "quantity": 3, "status": "cancelled"},
            {"id": 3, "event_id": 1, "quantity": 4, "status": "active"},
            {"id": 4, "event_id": 2, "quantity": 10, "status": "active"},
        ]),
    )

    assert OrderService.sold_tickets_for_event(1) == 6