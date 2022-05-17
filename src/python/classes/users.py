from enum import Enum

from src.python.services.database import DatabaseClass


class Role(Enum):
    ADMIN = "ADMIN"
    SENIOR = "SENIOR"
    JUNIOR = "JUNIOR"


class Users(DatabaseClass):
    def __init__(self, uid: int | None, login: str, password: str, role: Role, full_name: str, username: str,
                 created_on: str, modified_on: str):
        super().__init__(uid)
        self.login = login
        self.password = password
        self.role = role
        self.full_name = full_name
        self.username = username
        self.created_on = created_on
        self.modified_on = modified_on

    @staticmethod
    def required_keys() -> tuple:
        return "role", "full_name", "username", "created_on", "modified_on"

    def response_format(self) -> dict:
        temp_dict = self.get_base_dict()
        temp_dict.pop('password', None)

        return temp_dict
