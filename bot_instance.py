from telebot import TeleBot
import os
from dotenv import load_dotenv

load_dotenv()

bot = TeleBot(os.getenv("BOT_TOKEN"))