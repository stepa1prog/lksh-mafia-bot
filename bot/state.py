from enum import Enum
from typing import Dict, List


# Предполагается, что объект игры Game будет создаваться при вызове команды /create
# и будет присваиваться полю creating_game пользователя, который её создал.
# Далее, в процессе создания пользователем игры будет заполняться поле role_count.
# После того, как пользователь закончил создание игры, игре должен быть присвоен уникальный game_id,
# и после этого игра должна быть добавлена в game_by_id у State.
# Когда нужное количество пользователей присоединится к игре, нужно случайно распределить роли,
# отправить их игрокам, сбросить их статусы, а также удалить игру из game_by_id.


class Game:
    role_count: Dict[str, int]
    joined_user_ids: List[str]
    role_by_user_id: Dict[str, str]  # заполняется, когда игра начинается, то есть все игроки присоединились

    def __init__(self):
        self.role_count = dict()
        self.joined_user_ids = list()
        self.role_by_user_id = dict()


class UserStatus(Enum):
    NONE = 0
    JOINED = 1
    CREATING = 2
    JOINING = 3


class User:
    user_id: str
    status: UserStatus
    in_game_id: str or None  # str if status == JOINED and None otherwise
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
