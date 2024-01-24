import os
from datetime import datetime

from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove, Message
from django.core.management.base import BaseCommand
from django.core.cache import cache

from accounts.utils import generate_code
from accounts.crud import create_profile
from accounts.keyboards.default import get_contact_phone

bot = TeleBot(os.environ.get("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start(message: Message):
    """This function sends welcome message to user"""

    username = message.from_user.username
    bot.send_message(message.chat.id, f"Salom {username} 👋\n"
                                      f"Tramplin.uz ning rasmiy botiga xush kelibsiz!\n\n"
                                      f"⬇️ Kontaktingizni yuboring (tugmani bosib)",
                     reply_markup=get_contact_phone())


@bot.message_handler(content_types=["contact"])
def contact(message: Message):
    """This function creates profile for user and sends verification code to user and saves it to cache"""

    user_id = message.from_user.id
    if message.contact.user_id == message.from_user.id:
        create_profile(message.from_user.username, message.contact.phone_number, user_id)
        code = generate_code()
        bot.set_state(user_id, str(code))  # This line saves code to bot state for user
        cache.set(code, user_id, timeout=60)
        bot.send_message(message.chat.id, f"🔒 Kodingiz:\n`{code}`", parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.chat.id, f"🔑 Yangi kod olish uchun /login ni bosing")
    else:
        bot.send_message(message.chat.id, "Iltimos, o'zingizning kontaktingizni yuboring!")


@bot.message_handler(commands=["login"])
def login(message: Message):
    """This function check time before sending verification code to user if already exist and saves it to cache"""

    user_id = message.from_user.id
    now = datetime.now()
    code = bot.get_state(user_id)
    if code and cache.ttl(code) > now.second:
        bot.send_message(message.chat.id, f"Eski kodingiz hali ham kuchda ☝️",
                         reply_markup=ReplyKeyboardRemove())
    else:
        code = generate_code()
        cache.set(code, user_id, timeout=60)
        bot.send_message(message.chat.id, f"🔒 Kodingiz:\n `{code}`", parse_mode="Markdown",
                         reply_markup=ReplyKeyboardRemove())


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        bot.infinity_polling()
