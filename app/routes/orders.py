from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.auth import get_current_user
from app.schemas import OrderCreateRequest
from app.services.event_service import EventService
from app.services.order_service import OrderService


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders(current_user=Depends(get_current_user)):
    orders = OrderService.list_orders()
    if current_user["role"] == "admin":
        return orders
    return [order for order in orders if order["customer_username"] == current_user["username"]]


@router.post("")
def create_order(payload: OrderCreateRequest, current_user=Depends(get_current_user)):
    event = EventService.get_event(payload.event_id)
    if event is None or event.get("deleted", False):
        raise HTTPException(status_code=404, detail="Event not found")

    try:
        return OrderService.create_order(event, current_user["username"], payload.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{order_id}/cancel")
def cancel_order(order_id: int, current_user=Depends(get_current_user)):
    try:
        return OrderService.cancel_order(order_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404 if str(exc) == "Order not found" else 400, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))
