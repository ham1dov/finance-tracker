from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from lexicon.buttons import reply


async def main_menu_btns()->ReplyKeyboardMarkup:
    button_expense = KeyboardButton(text = reply['expenses'])
    button_incomes = KeyboardButton(text = reply['incomes'])
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                button_expense, button_incomes
            ]
        ]
    )
