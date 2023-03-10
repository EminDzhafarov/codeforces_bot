import logging
import sqlalchemy
import kb
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.sql.expression import func
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from sqlalchemy.orm import sessionmaker
from settings import API_TOKEN, DB_URL
from db.models import Task

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN) #Телеграм токен
dp = Dispatcher(bot=bot, storage=storage)

engine = sqlalchemy.create_engine(DB_URL)
connection = engine.connect()

Session = sessionmaker(bind=engine)

#Набор значений сложности для проверки
diffs = {800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000}

#Стейты FSM
class ClientStates(StatesGroup):
    get_diff = State()
    get_theme = State()
    result = State()

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message) -> None:
    await message.answer('Это бот для тестового задания.', reply_markup=kb.cont_kb)
    await ClientStates.get_diff.set()

@dp.message_handler(state=ClientStates.get_diff)
async def get_diff(message: types.Message, state: FSMContext):
    await message.answer('Выберите сложность задачи:', reply_markup=kb.start_kb)
    await ClientStates.get_theme.set()

@dp.message_handler(state=ClientStates.get_theme)
async def get_diff(message: types.Message, state: FSMContext):
    diff = message.text.strip()
    try:
        if int(diff) in diffs: #Проверяем, есть ли значение в списке сложностей
            await state.update_data(diff=diff)
            await message.answer('Выберите тему:', reply_markup=kb.theme_kb)
            await ClientStates.result.set()
        else:
            await message.answer('Ошибка')
    except ValueError:
        await message.answer('Ошибка')

@dp.message_handler(state=ClientStates.result)
async def get_theme(message: types.Message, state: FSMContext):
    theme = message.text.strip() #Берем тему из текста сообщения
    await state.update_data(theme=theme.lower())
    #Открываем сессию БД
    with Session.begin() as session:
        #Получаем полученные раннее данный из FSM
        data = await state.get_data()
        #Делаем из словаря полученных данных SQL запрос
        result = session.query(Task).filter(Task.diff == data['diff']).filter(Task.theme ==  data['theme'])\
            .order_by(func.random()).limit(10)
        #Проверяем, есть ли результат
        if session.query(Task).filter(Task.diff == data['diff']).filter(Task.theme ==  data['theme'])\
            .order_by(func.random()).first() is None:
            await message.answer('Ничего не найдено :(', reply_markup=kb.return_kb)
        else:
            #Выдаем результат
            await message.answer('Вот, что мне удалось найти:', \
                                 reply_markup=kb.return_kb)
            for t in result:
                await message.answer(f'Номер: {t.number}\n'\
                                     f'Название: <a href="{t.link}">{t.title}</a>\n'\
                                     f'Тема: {t.theme}\n'\
                                     f'Сложность: {t.diff}\n'\
                                     f'Решили: {t.solved}', \
                                     parse_mode='HTML', reply_markup=kb.return_kb)

        session.close() #Закрываем сессию
    await state.finish() #Обнуляем FSM
    await ClientStates.get_diff.set() #Ставим начальный стейт

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

