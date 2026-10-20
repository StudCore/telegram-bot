import functools
from db.db import execute, fetch_all, fetch_one
from telebot.types import Message
import time
from bot_instance import bot

def spam_interceptor(func):

    @functools.wraps(func)
    def handle_message(*args, **kwargs):

        message : Message = args[0]
        now = int(time.time())

        messages_amount = fetch_one(
            "SELECT COUNT(*) FROM message_log WHERE user_id = ? AND sent_at >= ?",
            (message.from_user.id, now - 120)
        )[0]

        if messages_amount > 10:

            execute("INSERT OR IGNORE INTO black_list(user_id) VALUES(?)", (message.from_user.id,))

        else:
            execute("INSERT INTO message_log(user_id, sent_at) VALUES(?, ?)", (message.from_user.id, int(time.time())))
            func(*args, **kwargs)

    return handle_message