import asyncio
import datetime
import asyncpg

from config.config import db_uri


class Users:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.pool = None  # Пул соединений будет создан в `connect()`

    async def connect(self):
        """Создает пул соединений с базой данных."""
        self.pool = await asyncpg.create_pool(dsn=self.db_uri, min_size=1, max_size=10)
        print("✅ Database connection pool created.")

    async def close_pool(self):
        """Закрывает пул соединений."""
        await self.pool.close()
        print("🔒 Database connection pool closed.")

    async def create_table_users(self):
        """Создает таблицу пользователей, если она не существует."""
        query = """CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            full_name VARCHAR
        )"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def add_user(self, id:int, full_name:str):
        query = """INSERT INTO users (id, full_name) VALUES ($1, $2)"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query, id, full_name)
    async def get_user(self, id:int):
        query = """SELECT * FROM users WHERE id = $1"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, id)

    async def create_table_expenses(self):
        query = """CREATE TABLE IF NOT EXISTS expenses(
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            name VARCHAR,
            amount FLOAT,
            date DATE
        )"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def get_all_transactions(self, mode:str):
        query = f"""SELECT * FROM {mode} WHERE TRUE"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query)

    async def add_new_expense(self, user_id, name:str, amount:float, date:datetime.date):
        query = """INSERT INTO expenses (user_id, name, amount, date) VALUES($1, $2, $3, $4)"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, name, amount, date)
    async def get_sum_of_transactions(self, interval:str,  mode:str, user_id:int, date1:datetime.date=None, date2:datetime.date=None):
        query = f"""SELECT SUM(amount) FROM {mode} WHERE user_id = $1 AND date BETWEEN $2 AND $3"""
        if interval =='today':
            query = f"""SELECT SUM(amount) FROM {mode} WHERE user_id = $1 AND date = $2"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            if interval=='today':
                return await conn.fetchrow(query, user_id, date2)
            else:
                return await conn.fetchrow(query, user_id,date1, date2)


    async def get_transactions(self, interval:str, user_id:int, mode:str, date1:datetime.date=None, date2:datetime.date=None, today:datetime.date=None):
        modes = ['expenses', 'incomes']

        interval = ['today', '3_days', 'week', 'month', 'year', 'default']
        query = f"""SELECT * FROM {mode} WHERE date BETWEEN $1 and $2"""

        if interval=='today':
            query = f"""SELECT * FROM {mode} WHERE user_id = $1 AND date = $2"""
        else:
            query = f"""SELECT * FROM {mode} WHERE user_id = $1 AND date BETWEEN $2 AND $3"""
        async with self.pool.acquire() as conn:
            if interval=='today':
                data = await conn.fetch(query, user_id, today)
            else:
                data = await conn.fetch(query, user_id, date1, date2)
            return data
    async def create_table_incomes(self):
        query = """CREATE TABLE IF NOT EXISTS incomes(
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            name VARCHAR,
            amount FLOAT,
            date DATE
        )"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def add_new_income(self, user_id, name:str, amount:float, date:datetime.date):
        query = """INSERT INTO incomes(user_id, name, amount, date) VALUES($1, $2, $3, $4)"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id, name, amount, date)

    async def get_incomes(self, user_id:int, mode:str, date_time1:datetime.date=None, date_time2:datetime.date=None, today:datetime.date=None):
        modes = ['today', '3_days', 'week', 'month', 'year', 'default']
        query = """SELECT * FROM incomes WHERE date BETWEEN $1 and $2"""
        if not self.pool:
            await self.connect()
        if mode == 'today':
            query = """SELECT * FROM incomes WHERE user_id = $1 AND date = $2"""
        else:
            query = """SELECT * FROM incomes WHERE user_id = $1 AND date BETWEEN $2 AND $3"""
        async with self.pool.acquire() as conn:
            if mode == 'today':
                data = await conn.fetch(query, user_id, today)
            else:
                data = await conn.fetch(query, user_id, date_time1, date_time2)
            return data
    async def drop_table_incomes(self):
        query = """DROP TABLE incomes"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)
    async def drop_table_expenses(self):
        query = """DROP TABLE expenses"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    async def drop_table_users(self):
        query = """DROP TABLE users"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            await conn.execute(query)


users = Users(db_uri=db_uri)
async def main():
    await users.create_table_users()
    users_ = await users.get_user(1231)
    print(users_)
    # await users.add_user(1231, '1231')

asyncio.run(main())