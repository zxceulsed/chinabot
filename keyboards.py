# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    buttons = [
        [KeyboardButton(text="🛒 Рассчитать стоимость товара"), KeyboardButton(text="👨‍💻 Связаться с менеджером")],
        [KeyboardButton(text="❓Часто задаваемые вопросы"), KeyboardButton(text="📌 Отзывы покупателей")],
        [KeyboardButton(text="📱 Наши соц.сети")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def FAQ_keyboard():
    buttons = [
        [KeyboardButton(text="Кто мы?")],
        [KeyboardButton(text="Как происходит расчёт?"), KeyboardButton(text="Стоимость и сроки доставки?")],
        [KeyboardButton(text="Как узнать нужный размер?")],
        [KeyboardButton(text="Вернуться в меню ⬅️️️")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def raschit_keyboard():
    buttons = [
        [KeyboardButton(text="Poizon"),KeyboardButton(text="Taobao"),KeyboardButton(text="1688")],
        [KeyboardButton(text="Pinduoduo"), KeyboardButton(text="95"),KeyboardButton(text="Другая площадка")],
        [KeyboardButton(text="Инструкция по установке приложений")],
        [KeyboardButton(text="Вернуться назад⬅️️️")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def nazad_v_menu_keyboard():
    buttons = [
        [KeyboardButton(text="🔙 Назад в меню")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def oform_keyboard():
    buttons = [
        [KeyboardButton(text="Оформить заказ 📝")],
        [KeyboardButton(text="🔙 Назад в меню")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def TOVAR_keyboard():
    buttons = [
        [KeyboardButton(text="Добавить товар")],
        [KeyboardButton(text="Удалить Товар")],
        [KeyboardButton(text="Отправить заявку менеджеру")],
        [KeyboardButton(text="Отменить заказ")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def society_keyboard():
    buttons = [
        [InlineKeyboardButton(text="VK", url="https://vk.com")],
        [InlineKeyboardButton(text="Instagram", url="https://instagram.com/example")],
        [InlineKeyboardButton(text="TikTok", url="https://tiktok.com")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)  # Передаём inline_keyboard явно
    return keyboard

def otzivi_keyboard():
    buttons = [
        [InlineKeyboardButton(text="В Telegram", url="https://Telegram.com")],
        [InlineKeyboardButton(text="В VK", url="https://VK.COM")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)  # Передаём inline_keyboard явно
    return keyboard

def get_inline_keyboard():
    buttons = [
        [InlineKeyboardButton(text="С пюрешкой", callback_data="with_puree")],
        [InlineKeyboardButton(text="Без пюрешки", callback_data="without_puree")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


