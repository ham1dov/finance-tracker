from aiogram.fsm.state import State, StatesGroup

class AddExpense(StatesGroup):
    Name = State()
    Amount = State()

class AddIncome(StatesGroup):
    Name = State()
    Amount = State()

