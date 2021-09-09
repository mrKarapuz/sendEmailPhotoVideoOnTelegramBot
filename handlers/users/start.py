
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import force_reply, video
from states import Send_Photo
from keyboards.default import continue_button, send_yet
from loader import dp
from functions.send_to_mail import *

@dp.message_handler(text='Отправить еще')
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!\nВведите информацио о машине (обязательно последние 4 цифры винкода')
    await Send_Photo.enter_the_information_on_car.set()
    

@dp.message_handler(state=Send_Photo.enter_the_information_on_car)
async def enter_the_information(message: types.Message, state: FSMContext):
    await state.update_data(car_information = message.text)
    folder_path = 'archives/' + str(message.from_user.id) + '/'
    try:
        os.mkdir(folder_path)
    except FileExistsError:
        pass
    data = await state.get_data()
    car_information = data.get('car_information')
    count = 0
    last_four_numbers_wincode = ''
    for elem in car_information:
        try:
            elem = int(elem)
        except ValueError:
            pass
        if type(elem) == int:
            last_four_numbers_wincode+=str(elem)
            count+=1
        elif elem == ' ' or type(elem) != int:
            count = 0
            last_four_numbers_wincode = ''
        if len(last_four_numbers_wincode) == 4:
            break
    if len(last_four_numbers_wincode) != 4:
        await message.answer(text='Не обнаружены последние 4 цифры винкода, убедитесь что они отделены пробелом от остальной информации\n/start - начать заново')
        await state.finish()
    else:
        await message.answer(text='Отправьте фото или видео и нажмите на кнопку "Продолжить"\nПожалуйста, дождитесь отправки фото', reply_markup=continue_button)
        await state.update_data(folder_path=folder_path, photo_ids=[], last_four_numbers_wincode=last_four_numbers_wincode)
        await Send_Photo.enter_the_car_media.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=Send_Photo.enter_the_car_media)
async def enter_the_photo(message: types.Message, state: FSMContext):
    
    photo_id = message.photo[-1].file_unique_id
    data = await state.get_data()
    photo_ids = [data.get('photo_ids')]
    photo_ids.append(message.photo[-1].file_id)
    await message.photo[-1].download('archives/' + str(message.from_user.id) + '/' + photo_id + '.jpg')
    await state.update_data(photo_ids = photo_ids)

@dp.message_handler(text='Продолжить', state=Send_Photo.enter_the_car_media)
async def enter_the_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get('photo_ids')
    folder_path = data.get('folder_path')
    if len(photo_ids) == 0:
        await message.answer('Вы не отправли медиа\n/start - начать заново')
        await state.finish()
        return 0
    last_four_numbers_wincode = data.get('last_four_numbers_wincode')
    await message.answer('Формирования архива и отправка сообщения...')
    do_zip_file(folder_path, last_four_numbers_wincode)
    await state.finish()
    await message.answer(text='Файлы были успешно отправлены', reply_markup=send_yet)

@dp.message_handler(text='Отмена', state=[Send_Photo.enter_the_car_media])
async def enter_the_photo(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text='Отменено\n/start - начать заново')