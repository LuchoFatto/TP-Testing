import pytest
from app.services.user_service import UserService


def test_register_customer_duplicate_user(monkeypatch):
    monkeypatch.setattr(UserService, "get_user", staticmethod(lambda username: {"username": username}))

    with pytest.raises(ValueError, match="Username already exists"):
        UserService.register_customer("customer1", "1234")