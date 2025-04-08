from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config.config import db_uri, admin_list
from config.misc import extract_amount, current_date
from database.manage_db import Users
from keyboards.inline.main_inline_buttons import expenses_btns, incomes_btns, interval_buttons
from keyboards.reply.main_menu_buttons import main_menu_btns
from lexicon.buttons import reply
from states.default import AddExpense, AddIncome
from zoneinfo import ZoneInfo
import datetime

user_router = Router()
users = Users(db_uri)

@user_router.message(CommandStart(), default_state)
async def start(message:Message, bot:Bot):
    user = await users.get_user(id=message.from_user.id)
    if not user:
        try:
            await users.add_user(id=message.from_user.id, full_name=message.from_user.full_name)
            await bot.send_message(chat_id=admin_list[0], text=f'New user: {message.from_user.full_name}',
                                   reply_markup=InlineKeyboardMarkup(
                                       inline_keyboard=[
                                           [
                                               InlineKeyboardButton(text=f'{message.from_user.full_name}', url=f'tg://user?id={message.from_user.id}')
                                           ]
                                       ]))
        except Exception as err:
            await bot.send_message(chat_id=admin_list[0], text=str(err))


    await message.answer(f'Добро пожаловать, <b>{message.from_user.full_name}</b>', reply_markup=await main_menu_btns())
    all_trs = await users.get_all_transactions(mode='expenses')
    print(all_trs)
    return

@user_router.message(F.text.in_([reply['expenses'], reply['incomes']]))
async def handle_texts(message:Message):
    message_text = message.text
    if message_text==reply['expenses']:
        await message.answer('Выберите', reply_markup=await expenses_btns())
    elif message_text==reply['incomes']:
        await message.answer('Выберите', reply_markup=await incomes_btns())
    else:
        pass

@user_router.callback_query(F.data.startswith('expenses:'))
async def handle_expenses(callback:CallbackQuery, state:FSMContext):
    option = callback.data.split(':')[-1]
    if option=='add':
        await callback.message.answer('На что ты потратил деньги?')
        await state.set_state(AddExpense.Name)
    elif option=='history':
        await callback.message.answer('Выбери интервал расходов.', reply_markup=await interval_buttons(mode='expenses'))
    return

@user_router.callback_query(F.data.startswith('incomes:'))
async def handle_incomes(callback:CallbackQuery, state:FSMContext):
    option = callback.data.split(':')[-1]
    if option=='add':
        await callback.message.answer('Откуда у тебя деньги взялись?')
        await state.set_state(AddExpense.Name)
    elif option=='history':
        await callback.message.answer('Выбери интервал приходов.', reply_markup=await interval_buttons(mode='incomes'))
        await state.set_state(AddIncome.Name)
    return

@user_router.message(F.content_type==ContentType.TEXT, AddIncome.Name)
async def get_new_income_name(message:Message, state:FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Сколько ты получил? ')
    await state.set_state(AddIncome.Amount)
    return

@user_router.message(F.content_type==ContentType.TEXT, AddIncome.Amount)
async def get_new_income_amount(message:Message, state:FSMContext, bot:Bot):
    amount = message.text
    amount = extract_amount(amount)
    if amount=='error':
        await message.answer('Сколько ты получил? В сумах.')
        await state.set_state(AddIncome.Amount)
        return
    data = await state.get_data()
    name = data.get('name')

    tashkent_time = datetime.datetime.now(ZoneInfo("Asia/Tashkent"))

    current_date = tashkent_time.date()
    try:
        await users.add_new_expense(user_id=message.from_user.id, name=name, amount=float(amount), date=current_date)
        await message.answer('Приход был успешно сохранен ✅')

    except Exception as err:
        await message.answer('Ооопс, что-то пошло не так. Попробуй позже заново')
        await bot.send_message(chat_id=admin_list[0], text=f'{err}')

    await state.clear()
    await message.answer('🏠 Главное меню', reply_markup=await main_menu_btns())
    return

@user_router.message(F.content_type==ContentType.TEXT, AddExpense.Name)
async def get_new_expense_name(message:Message, state:FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer('Сколько это стоило?')
    await state.set_state(AddExpense.Amount)
    return

@user_router.message(F.content_type==ContentType.TEXT, AddExpense.Amount)
async def get_new_expense_amount(message:Message, state:FSMContext, bot:Bot):
    amount = message.text
    amount = extract_amount(amount)
    if amount=='error':
        await message.answer('Сколько это стоило? В сумах.')
        await state.set_state(AddExpense.Amount)
        return
    data = await state.get_data()
    name = data.get('name')

    tashkent_time = datetime.datetime.now(ZoneInfo("Asia/Tashkent"))

    cur_date = tashkent_time.date()
    try:
        await users.add_new_expense(user_id=message.from_user.id, name=name, amount=float(amount), date=cur_date)
        await message.answer('Расход был успешно сохранен ✅')

    except Exception as err:
        await message.answer('Ооопс, что-то пошло не так. Попробуй позже заново')
        await bot.send_message(chat_id=admin_list[0], text=f'{err}')

    await state.clear()
    await message.answer('🏠 Главное меню', reply_markup=await main_menu_btns())
    return

@user_router.callback_query(F.data.startswith('interval:'))
async def handle_history(callback:CallbackQuery, state:FSMContext):
    mode = callback.data.split(':')[1]
    interval = callback.data.split(':')[-1]
    items = []
    get_sum = []
    cur_date = current_date()
    print(cur_date)
    if interval=='today':
        cur_date = current_date()
        get_sum = await users.get_sum_of_transactions(mode=mode, interval=interval, user_id=callback.from_user.id, date1=cur_date)
        items = await users.get_transactions(mode=mode, interval=interval, user_id=callback.from_user.id, today=cur_date)
    elif interval=='3days':
        cur_date = current_date()
        last_day = cur_date-datetime.timedelta(days=3)
        get_sum = await users.get_sum_of_transactions(mode=mode, interval=interval, user_id=callback.from_user.id,date1=last_day,
                                                      date2=cur_date)
        items = await users.get_transactions(mode=mode, interval='3days', user_id=callback.from_user.id, date1=last_day, date2=cur_date)
    elif interval=='week':
        today = current_date()
        weekday = today.weekday()
        monday =  today - datetime.timedelta(days=weekday)
        get_sum = await users.get_sum_of_transactions(mode=mode, interval=interval, user_id=callback.from_user.id,
                                                      date1=monday,
                                                      date2=today)
        items = await users.get_transactions(mode=mode, interval=interval, user_id=callback.from_user.id, date1=monday,
                                             date2=today)

    elif interval=='month':
        today = current_date()
        last_day = datetime.date.today().day
        get_sum = await users.get_sum_of_transactions(mode=mode, interval=interval, user_id=callback.from_user.id,
                                                      date1=today-datetime.timedelta(days=last_day),
                                                      date2=today)
        items = await users.get_transactions(mode=mode, interval=interval, user_id=callback.from_user.id, date1=today-datetime.timedelta(days=last_day),
                                             date2=today)
    elif interval=='year':
        today = current_date()
        year = current_date().year
        begin_year = datetime.date(day=1, month=1, year=year)
        get_sum = await users.get_sum_of_transactions(mode=mode, interval=interval, user_id=callback.from_user.id,
                                                      date1=begin_year,
                                                      date2=today)
        items = await users.get_transactions(mode=mode, interval=interval, user_id=callback.from_user.id, date1=begin_year, date2=current_date())
    print(items)
    if not items:
        await callback.message.answer(f'За этот период нет {"расходов" if mode=="expenses" else "приходов" if mode=="incomes" else "none"}')
        return

    interval_scale = {
        'today':'сегодня',
        '3days':'3 дня',
        'week':'неделю',
        'month':'месяц',
        'year':'год'
    }
    primary_text = (f'Ваши {"потратили" if mode=="expenses" else "заработали" if mode=="incomes" else "none"} '
                 f'{get_sum[0]} сумов 💸 за {interval_scale[interval]}.')

    secondary_text = ''
    for index, item in enumerate(items):
        secondary_text+=(f'№{index+1}.\n'
                         f'{"На что:" if mode=="expenses" else "Откуда:" if mode=="incomes" else "none"}: {item[2]}\n'
                         f'Сколько: {item[3]}\n'
                         f'Когда: {item[4]}\n')

    await callback.message.answer(primary_text+secondary_text)







