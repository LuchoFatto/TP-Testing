from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.auth import get_current_user
from app.schemas import CapacityUpdateRequest, EventCreateRequest, EventUpdateRequest
from app.services.event_service import EventService


router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
def list_events(active_only: bool = Query(default=True)):
    return EventService.list_events(active_only=active_only)


@router.get("/{event_id}")
def get_event(event_id: int):
    event = EventService.get_event(event_id)
    if event is None or event.get("deleted", False):
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("")
def create_event(payload: EventCreateRequest, current_user=Depends(get_current_user)):
    if current_user["role"] not in ("admin", "organizer"):
        raise HTTPException(status_code=403, detail="Only admin or organizer can create events")

    event = EventService.create_event(
        name=payload.name,
        date=payload.date,
        capacity=payload.capacity,
        price=payload.price,
        owner_username=current_user["username"],
    )
    return event


@router.put("/{event_id}")
def update_event(event_id: int, payload: EventUpdateRequest, current_user=Depends(get_current_user)):
    try:
        return EventService.update_event(event_id, payload.model_dump(), current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404 if str(exc) == "Event not found" else 400, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.delete("/{event_id}")
def delete_event(event_id: int, current_user=Depends(get_current_user)):
    try:
        return EventService.delete_event(event_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404 if str(exc) == "Event not found" else 409, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))


@router.patch("/{event_id}/deactivate")
def deactivate_event(event_id: int, current_user=Depends(get_current_user)):
    try:
        return EventService.deactivate_event(event_id, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))

@router.patch("/{event_id}/capacity")
def update_capacity(event_id: int, payload: CapacityUpdateRequest, current_user=Depends(get_current_user)):
    try:
        return EventService.update_capacity(event_id, payload.capacity, current_user)
    except ValueError as exc:
        raise HTTPException(status_code=404 if str(exc) == "Event not found" else 400, detail=str(exc))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc))