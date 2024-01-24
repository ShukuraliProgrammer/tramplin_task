import os
from datetime import datetime
from telebot import TeleBot
from telebot.types import ReplyKeyboardRemove
from django.core.management.base import BaseCommand
from django.core.cache import cache

from accounts.utils import generate_code
from accounts.crud import get_profile

from accounts.keyboards.default import get_contact_phone

bot = TeleBot(os.environ.get("BOT_TOKEN"))


@bot.message_handler(commands=["start"])
def start(message):
    username = message.from_user.username
    bot.send_message(message.chat.id, f"Salom {username} 👋\n"
                                      f"Tramplin.uz ning rasmiy botiga xush kelibsiz!\n\n"
                                      f"⬇️ Kontaktingizni yuboring (tugmani bosib)",
                     reply_markup=get_contact_phone())


@bot.message_handler(content_types=["contact"])
def contact(message):
    username = message.from_user.username
    phone = message.contact.phone_number
    if message.contact.user_id == message.from_user.id:
        code = generate_code()
        data = {
            "code": code,
            "phone": phone,
            "expires_in": datetime.now().replace(minute=+1),
        }
        cache.set(username, data, timeout=60)
        bot.send_message(message.chat.id, f"🔒 Kodingiz:\n`{code}`", parse_mode="Markdown")
        bot.send_message(message.chat.id, f"🔑 Ysngi kod olish uchun /login ni bosing")

    else:
        bot.send_message(message.chat.id, "Iltimos, o'zingizning kontaktingizni yuboring!")


@bot.message_handler(commands=["login"])
def login(message):
    username = message.from_user.username
    profile = get_profile(username)
    if username in cache:
        now = datetime.now()
        print("now: ", now)

        data = cache.get(username)
        print("data: ", data)
        print("expires in: ", cache.ttl(username))
        if cache.ttl(username) > now.second:
            bot.send_message(message.chat.id, f"Eski kodingiz hali ham kuchda ☝️",
                             reply_markup=ReplyKeyboardRemove())
        else:
            code = generate_code()
            new_data = {
                "code": code,
                "phone": data["phone"],
            }
            cache.set(username, new_data, timeout=60)
            bot.send_message(message.chat.id, f"🔒 Kodingiz:\n `{code}`", parse_mode="Markdown")
    elif profile:
        code = generate_code()
        new_data = {
            "code": code,
            "phone": profile.phone,
        }
        cache.set(username, new_data, timeout=60)
        bot.send_message(message.chat.id, f"🔒 Kodingiz:\n``{code}`", parse_mode="Markdown")
        bot.send_message(message.chat.id, f"🔑 Ysngi kod olish uchun /login ni bosing")
    else:
        bot.send_message(message.chat.id, f"Salom {username} 👋\n"
                                          f"Tramplin.uz ning rasmiy botiga xush kelibsiz!\n"
                                          f"⬇️ Kontaktingizni yuboring (tugmani bosib)",
                         reply_markup=get_contact_phone())


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        bot.infinity_polling()
