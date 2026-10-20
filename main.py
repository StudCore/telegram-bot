from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types
from dotenv import load_dotenv
import os
import random

load_dotenv()

state = {}
admins = list(map(lambda i: int(i), os.getenv("ADMINS").split(",")))

bot = TeleBot(os.getenv("BOT_TOKEN"))

def send_static(chat_id, file_name):

    text = ""
    
    with open(f"static/{file_name}.txt", "r") as f:

        text += f.read()

    bot.send_message(chat_id, text, parse_mode="markdown")

@bot.message_handler(commands=["start"])
def start(message : types.Message):

    send_static(message.chat.id, "onboarding")

@bot.message_handler(commands=["help"])
def help(message : types.Message):

    send_static(message.chat.id, "help")


@bot.message_handler(commands=["console"])
def console(message : types.Message):

    send_static(message.chat.id, "console")

    state[message.chat.id] = "console"

@bot.message_handler(commands=["donate"])
def donate(message : types.Message):

    send_static(message.chat.id, "donate")

@bot.message_handler(commands=["rules"])
def rules(message : types.Message):

    send_static(message.chat.id, "rules")

@bot.message_handler(content_types=['text', 'sticker', 'animation', 'photo', 'video', 'document', 'voice', 'audio', 'video_note'], func=lambda m: True)
def handle_messages(message : types.Message):

    chat_state = state.get(message.chat.id)

    if chat_state == "console":

        admin_index = random.randint(0, len(admins) - 1)

        bot.forward_message(admins[admin_index], from_chat_id=message.chat.id, message_id=message.id)
        state[message.chat.id] = ""
        bot.send_message(message.chat.id, "Кто то из админов получил ваше сообщение)\n\nЕсли оно ему понравилось, то он передаёт вам спасибо, если нет, то он скоро напишет вам...")

@bot.callback_query_handler(func=lambda c: True)
def handle_query(call : types.CallbackQuery):

    pass
    

bot.infinity_polling()