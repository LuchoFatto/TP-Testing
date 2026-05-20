from typing import Dict, List, Optional

from app.core.logger import logger
from app.repositories.file_repository import FileRepository


order_repository = FileRepository("orders.json")


class OrderService:
    @staticmethod
    def list_orders() -> List[Dict]:
        return order_repository.read_all()

    @staticmethod
    def get_order(order_id: int) -> Optional[Dict]:
        orders = order_repository.read_all()
        return next((o for o in orders if o["id"] == order_id), None)

    @staticmethod
    def list_orders_for_event(event_id: int) -> List[Dict]:
        orders = order_repository.read_all()
        return [o for o in orders if o["event_id"] == event_id]

    @staticmethod
    def event_has_any_orders(event_id: int) -> bool:
        return any(o["event_id"] == event_id for o in order_repository.read_all())

    @staticmethod
    def sold_tickets_for_event(event_id: int) -> int:
        orders = OrderService.list_orders()
        return sum(
            order["quantity"]
            for order in orders
            if order["event_id"] == event_id and order["status"] == "active"
        )

    @staticmethod
    def create_order(event: Dict, customer_username: str, quantity: int) -> Dict:
        logger.info(
            "Purchase started: event_id=%s customer=%s quantity=%s",
            event["id"],
            customer_username,
            quantity,
        )

        if quantity <= 0:
            logger.warning("Purchase rejected: quantity must be greater than zero")
            raise ValueError("Quantity must be greater than zero")

        if not event["active"] or event.get("deleted", False):
            logger.warning("Purchase rejected: event unavailable event_id=%s", event["id"])
            raise ValueError("Event is not available")

        sold_tickets = OrderService.sold_tickets_for_event(event["id"])
        available_tickets = event["capacity"] - sold_tickets

        if quantity > available_tickets:
            logger.warning(
                "Purchase rejected: insufficient capacity event_id=%s requested=%s available=%s",
                event["id"],
                quantity,
                available_tickets,
            )
            raise ValueError("Insufficient capacity")

        orders = order_repository.read_all()
        next_id = 1 if not orders else max(order["id"] for order in orders) + 1

        new_order = {
            "id": next_id,
            "event_id": event["id"],
            "customer_username": customer_username,
            "quantity": quantity,
            "status": "active",
        }
        orders.append(new_order)
        order_repository.write_all(orders)
        logger.info("Purchase created successfully: order_id=%s", next_id)
        return new_order

    @staticmethod
    def cancel_order(order_id: int, current_user: Dict) -> Dict:
        orders = order_repository.read_all()
        order = next((o for o in orders if o["id"] == order_id), None)

        if order is None:
            logger.warning("Cancel rejected: order not found order_id=%s", order_id)
            raise ValueError("Order not found")

        if current_user["role"] != "admin" and order["customer_username"] != current_user["username"]:
            logger.warning(
                "Cancel rejected: forbidden order_id=%s user=%s",
                order_id,
                current_user["username"],
            )
            raise PermissionError("You do not have permission to cancel this order")

        if order["status"] == "cancelled":
            logger.warning("Cancel rejected: order already cancelled order_id=%s", order_id)
            raise ValueError("Order is already cancelled")

        order["status"] = "cancelled"
        updated_orders = [
            order if existing["id"] == order_id else existing
            for existing in orders
        ]
        order_repository.write_all(updated_orders)
        logger.info("Order cancelled successfully: order_id=%s", order_id)
        return order
