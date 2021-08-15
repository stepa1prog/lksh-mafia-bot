from enum import Enum
from typing import Dict, List


class Game:
    role_count: Dict[str, int]
    started: bool
    joined_user_ids: List[str]
    role_by_user_id: Dict[str, str]  # заполняется, когда игра начинается, то есть все игроки присоединились

    def __init__(self):
        self.role_count = dict()
        self.started = False
        self.joined_user_ids = list()
        self.role_by_user_id = dict()


class UserStatus(Enum):
    NONE = 0
    IN_GAME = 1
    CREATING = 2
    JOINING = 3


class User:
    user_id: str
    status: UserStatus
    in_game_id: str or None  # str if status == IN_GAME and None otherwise
    creating_game: Game or None  # Game if status == CREATING and None otherwise

    def __init__(self, user_id):
        self.user_id = user_id
        self.status = UserStatus.NONE
        self.in_game_id = None
        self.creating_game = None


class State:
    game_by_id: Dict[str, Game]
    user_by_id: Dict[str, User]

    def __init__(self):
        self.game_by_id = dict()
        self.user_by_id = dict()

    def get_user(self, user_id: str):
        if user_id not in self.user_by_id:
            self.user_by_id[user_id] = User(user_id)
        return self.user_by_id[user_id]


state = State()
