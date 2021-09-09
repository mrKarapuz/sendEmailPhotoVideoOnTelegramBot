from aiogram.dispatcher.filters.state import State, StatesGroup

class Send_Photo(StatesGroup):
    enter_the_information_on_car = State()
    enter_the_car_media = State()
