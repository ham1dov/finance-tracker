import asyncio
import datetime
from datetime import timedelta

from config.config import db_uri
from config.misc import current_date
from database.manage_db import Users

# cur_date = current_date()
# print(cur_date-datetime.timedelta(days=3))
# print(datetime.date.weekday(datetime.date.today()))
# today = datetime.datetime.now().date()
#
# # Get the current weekday (Monday is 0, Sunday is 6)
# weekday = today.weekday()
#
# # Calculate the date of the most recent Monday
# monday = today - timedelta(days=weekday)
#
# # Optional: Print range
# print(f"This week is from {monday} to {today}")
day1 = '2025-01-00'

date = datetime.date(day=1, month=1, year=2025)
# print(type(date))

# async def get_all_transactions():
#     users = Users(db_uri)
#     all_trnscs = await users.get_all_transactions(mode='expenses')
#     print(all_trnscs)
#
# asyncio.run(get_all_transactions())