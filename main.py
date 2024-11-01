from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = "Enter your key from botfather"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
'''kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)'''
kb = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb.add(button1)
kb.add(button2)

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    await message.answer(f'Выберите опцию:', reply_markup=kb)

@dp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    await call.answer(f'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Выберите опцию', reply_markup=kb)

@dp.callback_query_handler(text = "calories")
async def set_age(call):
    await call.answer(f'Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=float(message.text))
    await message.answer(f'Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=float(message.text))
    await message.answer(f'Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=float(message.text))
    data = await state.get_data()
    womenresult = (10*data['third']) + (6.25*data['second']) - (5*data['first']) - 161
    await message.answer( f'результат подсчета необходимого количества :{womenresult} каллорий')
    await state.finish()



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)