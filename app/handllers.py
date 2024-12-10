
import emoji

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, callback_query, InputFile
from app.pygithub import upload_to_github
import aiohttp
import app.keyboards as kb
from app import database as db
import os
from dotenv import load_dotenv
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.filters.logic import or_f

load_dotenv()
bot = Bot(token=os.getenv('API_TOKEN'))
password = os.getenv("PASSWORD")

router = Router()

class Test(StatesGroup):
    fav_subj = State()
    skills = State()
    develop_skills = State()
    favorite_tasks = State()
    free_time = State()
    future_profession = State()

#Старт
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    await db.remember_me(user_id)
    answer = f'<b>Вітаємо </b>{user_name}!\nПропонуємо нашу допомогу з вибору профілю для майбутніх Десятикласників.'
    # await message.answer(
    #     f"Вітаємо {user_name}!\nПропонуємо нашу допомогу з вибору профілю для майбутніх Десятикласників.",
    #     reply_markup=kb.main)
    await message.answer(answer, parse_mode='HTML',reply_markup=kb.main)


# Адмін панель (по паролю)
@router.message(Command(f'{password}'))
async def admin_panel(message: Message):
    user_name = message.from_user.first_name
    await message.answer(f"Вітаємо {user_name}! Адмін панель активовано.",
                         reply_markup=kb.admin)

class ProfileStates(StatesGroup):
    step = State()

@router.message(or_f((F.text == emoji.emojize("Перелік профілів 📋")),(F.text == '/profiles')))
async def profiles(message: Message, state: FSMContext):
    profiles_list = await db.get_profiles()
    if not profiles_list:
        await message.answer("Профілі не знайдені.")
        return


    await state.set_state(ProfileStates.step)
    await state.update_data(step=0)


    response = (
        f"<b>Назва профілю:</b> {profiles_list[0]['profile_name']}\n"
        f"<b>Інформація:</b> {profiles_list[0]['profile_info']}"
    )
    await message.answer(response, parse_mode='HTML', reply_markup=kb.profile_catalog )


@router.callback_query(F.data == "next")
async def about_next(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    step = data.get("step", 0) + 1
    print(step)

    profiles_list = await db.get_profiles()
    if step < len(profiles_list):
        response = (
            f"<b>Назва профілю:</b> {profiles_list[step]['profile_name']}\n"
            f"<b>Інформація:</b> {profiles_list[step]['profile_info']}"
        )
        await callback_query.message.edit_text(response, parse_mode='HTML', reply_markup=kb.profile_catalog )

        await state.update_data(step=step)
    else:
        await callback_query.answer("Більше профілів немає.")

@router.callback_query(F.data == "back")
async def about_next(callback_query: CallbackQuery, state: FSMContext):

    profiles_list = await db.get_profiles()
    data = await state.get_data()
    step = data.get("step", len(profiles_list)) - 1
    print(step)

    if step >= 0:
        response = (
            f"<b>Назва профілю:</b> {profiles_list[step]['profile_name']}\n"
            f"<b>Інформація:</b> {profiles_list[step]['profile_info']}"
        )
        await callback_query.message.edit_text(response, parse_mode='HTML', reply_markup=kb.profile_catalog )

        await state.update_data(step=step)
    else:
        await callback_query.answer("Більше профілів немає.")

class Call_Schedule(StatesGroup):
    photo = State()
@router.message(F.text == 'Час прийому')
async def call_schedule_admin(message: Message, state: FSMContext):
    await message.answer("Пришліть фото часу прийому")
    await state.set_state(Call_Schedule.photo)

@router.message(Call_Schedule.photo)
async def call_schedule_set_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await db.execute_query("""
            INSERT INTO time_vizit (photo_id) VALUES (%s)
        """, (photo_id,))

    file_info = await bot.get_file(photo_id)
    file_path = file_info.file_path

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.telegram.org/file/bot{os.getenv('BOT_API')}/{file_path}") as resp:
            if resp.status == 200:
                file_content = await resp.read()
                file_name = f"{photo_id}.jpg"
                photo_url = f"https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/refs/heads/main/photos/{photo_id}.jpg"
                result = upload_to_github(file_name, file_content)
                await message.answer_photo(photo=photo_url)
            else:
                await message.answer("Не вдалось скачати фото.")
    await message.answer("Фото збережено в базі")



# Соціальні мережі
@router.message(F.text == f'Соціальні мережі 🌐')
async def socials(message: Message):
    await message.answer(f"Соціальні мережі: \n", reply_markup=kb.socials_networks)


# Про нас
@router.message(F.text == f'Про нас 🏫')
async def about_us(message: Message):
    await message.answer(f"""<b>Комунальний заклад загальної середньої освіти \n“Ліцей №3 імені Артема МазураХмельницької міської ради”</b>\n\nВ Ліцеї №3 імені Артема Мазура працюють відомі вчителі, автори підручників та посібників,\nнаставники переможців олімпіад,\nконкурсу-захисту МАН і спортивних змагань...<a href='http://tbl.km.ua/'>далі</a>\n\n""",reply_markup=kb.about, parse_mode='HTML')


# Налаштування
@router.message(F.text == 'Час прийому 🕓')
async def settings(message: Message):
    #await message.answer(f"Налаштування")
    photo = await db.execute_query("""
        SELECT photo_id FROM result_profile BY id DESC LIMIT 1
    """,fetch="fetchone")
    if photo:
        print(photo, "     1")
        photo = f'https://raw.githubusercontent.com/skachpro/photos_lyceum_bot/master/{photo['photo_id']}.jpg'

    else:
        print(photo, "     2")
    await message.answer_photo(photo=photo)

# Почати Тестування
@router.message(F.text == f"Почати тестування 💼")
async def start_test(message: Message, state:FSMContext):
    await message.answer("Тестування почато.")
    await state.set_state(Test.fav_subj)
    await message.answer("1. Оберіть улюблений предмет.", reply_markup=kb.test_subj)


#Початок Відлову відповідей
@router.callback_query(Test.fav_subj)
async def que1(callback_query: CallbackQuery, state: FSMContext):
    # user_id = callback_query.from_user.id
    answer = callback_query.data
    # await db.add_subj(answer, user_id)
    await state.update_data(fav_subj=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await state.set_state(Test.skills)
    await callback_query.message.edit_text(f"2. Що вам вдається найкраще?", reply_markup=kb.skills)

@router.callback_query(Test.skills)
async def que2(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data
    await state.update_data(skills=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await state.set_state(Test.develop_skills)
    await callback_query.message.edit_text(f"3. Які навички хочете розвивати?", reply_markup=kb.develop_skills)

@router.callback_query(Test.develop_skills)
async def que3(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data
    await state.update_data(develop_skills=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await state.set_state(Test.favorite_tasks)
    await callback_query.message.edit_text(f"4. Які завдання вам найбільше подобається виконувати?", reply_markup=kb.favorite_tasks)

@router.callback_query(Test.favorite_tasks)
async def que3(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data
    await state.update_data(favorite_tasks=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await state.set_state(Test.free_time)
    await callback_query.message.edit_text(f"5. Як проводите вільний час?", reply_markup=kb.free_time)

@router.callback_query(Test.free_time)
async def que4(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data
    await state.update_data(free_time=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await state.set_state(Test.future_profession)
    await callback_query.message.edit_text(f"6. Ким хочете працювати?", reply_markup=kb.future_profession)

@router.callback_query(Test.future_profession)
async def test_end(callback_query: CallbackQuery, state: FSMContext):
    answer = callback_query.data
    await state.update_data(future_profesion=answer)
    await callback_query.answer(f'Відповідь зараховано')
    await callback_query.message.edit_text(f"Тест Завершено!")
    data = await state.get_data()
    math = 0
    it = 0
    history = 0
    law = 0
    geography = 0
    chem_bio = 0
    ukr_philo = 0
    foreign_philo = 0
    sports_military = 0
    art = 0
    #await callback_query.message.answer(", ".join(map(str, data.values())))
    for value in data.values():
        if value == 'math':
            math += 1
        elif value == 'it':
            it += 1
        elif value == 'history':
            history += 1
        elif value == 'geography':
            geography += 1
        elif value == 'chem_bio':
            chem_bio += 1
        elif value == 'ukr_philo':
            ukr_philo += 1
        elif value == 'law':
            law += 1
        elif value == 'foreign_philo':
            foreign_philo += 1
        elif value == 'sports_military':
            sports_military += 1
        elif value == 'art':
            art += 1

    await callback_query.message.edit_text(
        f"<b>Схильність до:</b>\n"
        f"<code>Математики: {math * 16}%\n"
        f"Інформатики: {it * 16}%\n"
        f"Історії: {history * 16}%\n"
        f"Географії: {geography * 16}%\n"
        f"Хімії/Біології: {chem_bio * 16}%\n"
        f"Української філології: {ukr_philo * 16}%\n"
        f"Правового профілю: {law * 16}%\n"
        f"Іноземної філології: {foreign_philo * 16}%\n"
        f"Військово/Спортивного профілю: {sports_military * 16}%\n"
        f"Художньо-Естетичного профілю: {art * 16}%</code>",
        parse_mode="html"
    )
    data = {
        "Математика": math * 16,
        "Інформатика": it * 16,
        "Історія": history * 16,
        "Географія": geography * 16,
        "Хімія/Біологія": chem_bio * 16,
        "Українська філологія": ukr_philo * 16,
        "Правовий профіль": law * 16,
        "Іноземна філологія": foreign_philo * 16,
        "Військово/Спортивний профіль": sports_military * 16,
        "Художньо-Естетичний профіль": art * 16
    }
    await state.clear()




# Адмін Панель - Додавання профілю
# @router.message(F.text == 'Адмін Панель')
# async def admin_panel_add_profile(message: Message):
#     await message.answer("Адмін Панель Активовано", reply_markup=kb.admin_kbd)
#
#     await message.answer("Введіть Назву Профілю:")
#     profile_name = (await bot.wait_for('message')).text
#
#     await message.answer("Введіть Інформацію про профіль:")
#     profile_info = (await bot.wait_for('message')).text
#
#     await db.add_profile(profile_name, profile_info)
#     await message.answer(
#         f"Операція Відбулась.\nДодано:\nНазва Профілю: {profile_name}\nІнформація про профіль: {profile_info}")


# Вийти з Адмін панелі
@router.message(F.text == 'Вийти з Адмін панелі')
async def leave_admin(message: Message):
    await cmd_start(message)
