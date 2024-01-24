from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def get_contact_phone():
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button = KeyboardButton(text="☎️ Telefon raqamni yuborish", request_contact=True)
    keyboard.add(button)
    return keyboard
