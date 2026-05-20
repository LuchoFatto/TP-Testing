from typing import Dict, List, Optional

from app.core.logger import logger
from app.repositories.file_repository import FileRepository


user_repository = FileRepository("users.json")


class UserService:
    @staticmethod
    def list_users() -> List[Dict]:
        return user_repository.read_all()

    @staticmethod
    def get_user(username: str) -> Optional[Dict]:
        users = user_repository.read_all()
        return next((u for u in users if u["username"] == username), None)

    @staticmethod
    def register_customer(username: str, password: str) -> Dict:
        if UserService.get_user(username) is not None:
            logger.warning("Register rejected: username already exists (%s)", username)
            raise ValueError("Username already exists")

        users = user_repository.read_all()
        new_user = {
            "username": username,
            "password": password,
            "role": "customer"
        }
        users.append(new_user)
        user_repository.write_all(users)
        logger.info("Customer registered successfully: username=%s", username)
        return new_user

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict]:
        user = UserService.get_user(username)
        if user is None:
            logger.warning("Login rejected: unknown user (%s)", username)
            return None

        if user["password"] != password:
            logger.warning("Login rejected: invalid password (%s)", username)
            return None

        logger.info("Login successful: username=%s role=%s", username, user["role"])
        return user
