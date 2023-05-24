from loguru import logger
from pydantic import BaseModel, parse_obj_as
from .database import _MongoClient


class User(BaseModel):
    username: str
    hashed_password: str


class NewUser(BaseModel):
    username: str
    password: str


class _UserService(_MongoClient):
    """User Service"""

    def __init__(self) -> None:
        super().__init__()
        self.users_collection = self.db["users"]

    @staticmethod
    def _hash_password(password: str) -> str:
        return password + "@1234"

    def _match_password(self, password: str, hashed_password: str) -> bool:
        logger.info(f"{password}, {hashed_password}, {self._hash_password(password)}")
        return self._hash_password(password) == hashed_password

    async def list_all(self) -> list[User]:
        return parse_obj_as(
            list[User],
            await self.users_collection.find({}, {"_id": 0}).to_list(length=None),  # type: ignore
        )

    async def exists(self, key: str, value: str) -> bool:
        return bool(await self.users_collection.find_one({key: value}))

    async def create(self, data: NewUser) -> None:
        if await self.exists("username", data.username):
            raise Exception("User already exists")

        await self.users_collection.insert_one(
            {
                "username": data.username,
                "hashed_password": self._hash_password(data.password),
            }
        )

    async def single(self, username: str, throw: bool = False) -> User | None:
        """Retrieve user from db and raise exception if not found (if specified)."""
        user = await self.users_collection.find_one({"username": username}, {"_id": 0})
        if not user and throw:
            raise Exception("User not found.")
        return parse_obj_as(User | None, user)

    async def authorize(self, data: NewUser) -> str:
        """Retrieve token for given user."""
        user = await self.single(data.username, throw=True)
        assert user is not None, "User not found"
        if not self._match_password(data.password, user.hashed_password):
            raise Exception("wrong credentials.")

        # XXX: Fakehash, need JWT here. Replace ASAP.
        return user.username + "_" + user.hashed_password

    async def verify_token(self, token: str) -> User:
        """Verify token."""
        username, *_ = token.split("_")
        # XXX: Need to verify password too.
        user = await self.single(username, throw=True)
        assert user, "User not found."

        return user
