import functools
from db.db import execute, fetch_all, fetch_one
from telebot.types import Message
import time
from bot_instance import bot

def blacklist_checker(func):

    @functools.wraps(func)
    def handle_message(*args, **kwargs):

        is_user_blocked = fetch_one("SELECT EXISTS(SELECT 1 FROM black_list)")

        if is_user_blocked:

            return

        else:
            func(*args, **kwargs)

    return handle_message