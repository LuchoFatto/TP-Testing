import pytest
from app.services.order_service import OrderService


def test_cancel_order_already_cancelled(monkeypatch):
    orders = [
        {
            "id": 1,
            "event_id": 1,
            "customer_username": "customer1",
            "quantity": 2,
            "status": "cancelled",
        }
    ]

    monkeypatch.setattr(
        "app.services.order_service.order_repository.read_all",
        lambda: orders
    )

    with pytest.raises(ValueError, match="already cancelled"):
        OrderService.cancel_order(1, {"username": "customer1", "role": "customer"})