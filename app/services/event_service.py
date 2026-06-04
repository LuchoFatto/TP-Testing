from typing import Dict, List, Optional

from app.core.logger import logger
from app.repositories.file_repository import FileRepository
from app.services.order_service import OrderService


event_repository = FileRepository("events.json")


class EventService:
    @staticmethod
    def list_events(active_only: bool = True) -> List[Dict]:
        events = event_repository.read_all()
        visible_events = [e for e in events if not e.get("deleted", False)]

        if active_only:
            visible_events = [e for e in visible_events if e["active"]]

        logger.info("Returned %s events", len(visible_events))
        return visible_events

    @staticmethod
    def list_all_events() -> List[Dict]:
        return event_repository.read_all()

    @staticmethod
    def get_event(event_id: int) -> Optional[Dict]:
        events = event_repository.read_all()
        return next((e for e in events if e["id"] == event_id), None)

    @staticmethod
    def create_event(name: str, date: str, capacity: int, price: float, owner_username: str) -> Dict:
        events = event_repository.read_all()
        next_id = 1 if not events else max(event["id"] for event in events) + 1

        new_event = {
            "id": next_id,
            "name": name,
            "date": date,
            "capacity": capacity,
            "price": price,
            "active": True,
            "deleted": False,
            "owner_username": owner_username,
        }
        events.append(new_event)
        event_repository.write_all(events)
        logger.info("Event created successfully: event_id=%s owner=%s", next_id, owner_username)
        return new_event

    @staticmethod
    def update_event(event_id: int, payload: Dict, current_user: Dict) -> Dict:
        event = EventService.get_event(event_id)
        if event is None or event.get("deleted", False):
            raise ValueError("Event not found")

        if current_user["role"] != "admin" and event["owner_username"] != current_user["username"]:
            raise PermissionError("You do not have permission to update this event")

        sold_tickets = OrderService.sold_tickets_for_event(event_id)
        if payload["capacity"] < sold_tickets:
            raise ValueError("Capacity cannot be lower than sold tickets")

        event.update(payload)
        events = event_repository.read_all()
        updated_events = [event if existing["id"] == event_id else existing for existing in events]
        event_repository.write_all(updated_events)
        logger.info("Event updated successfully: event_id=%s", event_id)
        return event

    @staticmethod
    def deactivate_event(event_id: int, current_user: Dict) -> Dict:
        event = EventService.get_event(event_id)
        if event is None or event.get("deleted", False):
            raise ValueError("Event not found")

        if current_user["role"] != "admin" and event["owner_username"] != current_user["username"]:
            raise PermissionError("You do not have permission to deactivate this event")

        event["active"] = False
        events = event_repository.read_all()
        updated_events = [event if existing["id"] == event_id else existing for existing in events]
        event_repository.write_all(updated_events)
        logger.info("Event deactivated successfully: event_id=%s", event_id)
        return event

    @staticmethod
    def delete_event(event_id: int, current_user: Dict) -> Dict:
        event = EventService.get_event(event_id)
        if event is None or event.get("deleted", False):
            raise ValueError("Event not found")

        if current_user["role"] != "admin" and event["owner_username"] != current_user["username"]:
            raise PermissionError("You do not have permission to delete this event")

        event["deleted"] = True
        event["active"] = False
        events = event_repository.read_all()
        updated_events = [event if existing["id"] == event_id else existing for existing in events]
        event_repository.write_all(updated_events)
        logger.info("Event deleted successfully: event_id=%s", event_id)
        return event

    @staticmethod
    def update_capacity(event_id: int, new_capacity: int, current_user: Dict) -> Dict:

        event = EventService.get_event(event_id)
        
        if event is None or event.get("deleted", False):
            raise ValueError("Event not found")

        if current_user["role"] != "admin" and event["owner_username"] != current_user["username"]:
            raise PermissionError("You do not have permission to update this event")

        sold_tickets = OrderService.sold_tickets_for_event(event_id)
        
        if new_capacity < sold_tickets:
            raise ValueError("Capacity cannot be lower than sold tickets")

        event["capacity"] = new_capacity
        events = event_repository.read_all()
        updated_events = [event if existing["id"] == event_id else existing for existing in events]
        event_repository.write_all(updated_events)
        logger.info("Event capacity updated successfully: event_id=%s new_capacity=%s", event_id, new_capacity)
        return event
