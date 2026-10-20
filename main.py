from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from telebot import types
from dotenv import load_dotenv
import os
import random
from utils.spam_interceptor import spam_interceptor
from bot_instance import bot
from utils.blacklist_checker import blacklist_checker
import functools
from db.db import fetch_one, execute, fetch_all

load_dotenv()

state = {}
admins = list(map(lambda i: int(i), os.getenv("ADMINS").split(",")))

def group_selector(func):

    @functools.wraps(func)
    def handle_message(*args, **kwargs):

        message : Message = args[0]

        user_group = fetch_one('SELECT "group" FROM groups WHERE user_id = ?', (message.from_user.id,))[0]

        if user_group == None:

            state[message.from_user.id] = "select group"
            bot.send_message(message.from_user.id, "Отправь номер своей группы чтобы мы показали список ближайших работ и ответы к ним")
            return

        func(*args, **kwargs)

    return handle_message

def send_static(chat_id, file_name):

    text = ""
    
    with open(f"static/{file_name}.txt", "r") as f:

        text += f.read()

    bot.send_message(chat_id, text, parse_mode="markdown")

@bot.message_handler(commands=["start"])
@blacklist_checker
@spam_interceptor
def start(message : types.Message):

    send_static(message.chat.id, "onboarding")

@bot.message_handler(commands=["help"])
@blacklist_checker
@spam_interceptor
def help(message : types.Message):

    send_static(message.chat.id, "help")


@bot.message_handler(commands=["console"])
@blacklist_checker
@spam_interceptor
def console(message : types.Message):

    send_static(message.chat.id, "console")

    state[message.chat.id] = "console"

@bot.message_handler(commands=["donate"])
@blacklist_checker
@spam_interceptor
def donate(message : types.Message):

    send_static(message.chat.id, "donate")

@bot.message_handler(commands=["answers"])
@blacklist_checker
@spam_interceptor
@group_selector
def answers(message : types.Message):

    keyboard = InlineKeyboardMarkup()
    b1 = InlineKeyboardButton("Контрольная по истории", callback_data="test")

    keyboard.add(b1)

    bot.send_message(message.from_user.id, reply_markup=keyboard)

@bot.message_handler(commands=["rules"])
@blacklist_checker
@spam_interceptor
def rules(message : types.Message):

    send_static(message.chat.id, "rules")

@bot.message_handler(content_types=['text', 'sticker', 'animation', 'photo', 'video', 'document', 'voice', 'audio', 'video_note'], func=lambda m: True)
@blacklist_checker
@spam_interceptor
def handle_messages(message : types.Message):

    chat_state = state.get(message.chat.id)

    if chat_state == "console":

        admin_index = random.randint(0, len(admins) - 1)

        bot.forward_message(admins[admin_index], from_chat_id=message.chat.id, message_id=message.id)
        state[message.chat.id] = ""
        bot.send_message(message.chat.id, "Кто то из админов получил ваше сообщение)\n\nЕсли оно ему понравилось, то он передаёт вам спасибо, если нет, то он скоро напишет вам...")

    if chat_state == "select group":

        group = 0

        try:
            group = int(message.text)

        except:

            bot.send_message(message.from_user.id, "Некорректный формат группы. Это четырёхзначное число.")

        execute('INSERT INTO groups(user_id, "group") VALUES(?, ?)', (message.from_user.id, group))


@bot.callback_query_handler(func=lambda c: True)
def handle_query(call : types.CallbackQuery):

    pass
    

bot.infinity_polling()