from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)


class LoginRequest(BaseModel):
    username: str
    password: str


class EventCreateRequest(BaseModel):
    name: str
    date: str
    capacity: int = Field(gt=0)
    price: float = Field(gt=0)


class EventUpdateRequest(BaseModel):
    name: str
    date: str
    capacity: int = Field(gt=0)
    price: float = Field(gt=0)
    active: bool


class CapacityUpdateRequest(BaseModel):
    capacity: int = Field(gt=0)


class OrderCreateRequest(BaseModel):
    event_id: int
    quantity: int = Field(gt=0)
