from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.buttons import inline


async def expenses_btns()->InlineKeyboardMarkup:
    button_add = InlineKeyboardButton(text=inline['expenses']['add'], callback_data='expenses:add')
    button_history = InlineKeyboardButton(text=inline['expenses']['history'], callback_data='expenses:history')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                button_add
            ],
            [
                button_history
            ]
        ]
    )


async def incomes_btns()->InlineKeyboardMarkup:
    button_add = InlineKeyboardButton(text=inline['incomes']['add'], callback_data='incomes:add')
    button_history = InlineKeyboardButton(text=inline['incomes']['history'], callback_data='incomes:history')
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                button_add
            ],
            [
                button_history
            ]
        ]
    )

async def interval_buttons(mode:str)->InlineKeyboardMarkup:
    modes = ['expenses', 'incomes']
    button_today = InlineKeyboardButton(text='Сегодня 📍', callback_data=f'interval:{mode}:today')
    button_3days = InlineKeyboardButton(text='3 дня', callback_data=f'interval:{mode}:3days')
    button_week = InlineKeyboardButton(text='Неделя', callback_data=f'interval:{mode}:week')
    button_month = InlineKeyboardButton(text='Месяц', callback_data=f'interval:{mode}:month')
    button_year = InlineKeyboardButton(text='Год', callback_data=f'interval:{mode}:year')
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            button_today
        ],
        [
            button_3days, button_week
        ],
        [
            button_month, button_year
        ]
    ])
