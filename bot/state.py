import random
import string

from enum import Enum
from typing import Dict, List, Set

from telegram import Update

import bot.messages as messages

# Предполагается, что объект игры Game будет создаваться при вызове команды /create
# и будет присваиваться полю creating_game пользователя, который её создал.
# Далее, в процессе создания пользователем игры будет заполняться поле roles.
# После того, как пользователь закончил создание игры, игре должен быть присвоен уникальный game_id,
# и после этого игра должна быть добавлена в game_by_id у State.
# Когда нужное количество пользователей присоединится к игре, метод start_game начнёт игру и
# разошлёт сообщения всем игрокам. После старта игры, её надо удалить из game_by_id у state.


class Game:
    game_id: str or None
    roles: List[str]
    joined_user_ids: List[str]
    role_by_user_id: Dict[str, str]  # заполняется, когда игра начинается, то есть все игроки присоединились

    def __init__(self):
        self.game_id = None
        self.roles = list()
        self.joined_user_ids = list()
        self.role_by_user_id = dict()

    def start_game(self, update: Update):
        random.shuffle(self.roles)
        for i in range(len(self.roles)):
            self.role_by_user_id[self.joined_user_ids[i]] = self.roles[i]

        for user_id in self.role_by_user_id.keys():
            update.message.bot.send_message(
                chat_id=user_id,
                text=messages.GAME_START.format(role=self.role_by_user_id[user_id])
            )
            state.get_user(user_id).status = UserStatus.NONE
            state.get_user(user_id).in_game_id = None


class UserStatus(Enum):
    NONE = 0
    JOINED = 1
    CREATING = 2
    JOINING = 3


# Предполагается, что каждому пользователю соответствуеет клас User. status задаёт то, что сейчас делает пользователь.
# Если пользователь ничего не делает, то статус NONE.
# Если пользователь начал создавать игру, то у него стоит статус CREATING.
# Если пользователь начал присоединяться к игре, то у него стоит статус JOINING.
# Если пользователь присоединился к игре или создал игру (в этом случае он автоматически должен присоединиться к игре),
# то у пользователья стоит статус JOINED.
# in_game_id задаёт id игры, к которой пользователь присоединился, если у него статус JOINED
# creating_game хранит структуру той игры, которую пользователь сейчас создаёт.

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

    def join_game(self, game: Game):
        game.joined_user_ids.append(self.user_id)
        self.status = UserStatus.JOINED
        self.in_game_id = game.game_id

    def clear_status(self):
        if self.in_game_id is not None:
            game = state.game_by_id[self.in_game_id]
            game.joined_user_ids.remove(self.user_id)
        self.in_game_id = None
        self.status = UserStatus.NONE


class State:
    game_by_id: Dict[str, Game]
    user_by_id: Dict[str, User]
    used_game_ids = Set[str]

    def __init__(self):
        self.game_by_id = dict()
        self.user_by_id = dict()
        self.used_game_ids = set()

    def get_user(self, user_id: str):
        if user_id not in self.user_by_id:
            self.user_by_id[user_id] = User(user_id)
        return self.user_by_id[user_id]

    def generate_game_id(self):

        def gen_random_string(n: int):
            return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))

        length = 2
        game_id = gen_random_string(length)

        while game_id in self.used_game_ids:
            length += 1
            game_id = gen_random_string(length)

        self.used_game_ids.add(game_id)
        return game_id


state = State()
