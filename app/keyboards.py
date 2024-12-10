from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import emoji


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"Перелік профілів {emoji.emojize(':clipboard:')}"), KeyboardButton(text=f"Соціальні мережі {emoji.emojize(':globe_with_meridians:')}")],
    [KeyboardButton(text=f"Про нас {emoji.emojize(':school:')}"), KeyboardButton(text='Час прийому 🕓')],
    [KeyboardButton(text=f"Почати тестування {emoji.emojize(':briefcase:')}")]
],
input_field_placeholder="Оберіть дію"
)

admin = ReplyKeyboardMarkup(keyboard=[
[KeyboardButton(text=f"Перелік профілів {emoji.emojize(':clipboard:')}"), KeyboardButton(text=f"Соціальні мережі {emoji.emojize(':globe_with_meridians:')}")],
    [KeyboardButton(text=f"Про нас {emoji.emojize(':school:')}"), KeyboardButton(text='Час прийому 🕓')],
    [KeyboardButton(text=f"Почати тестування {emoji.emojize(':briefcase:')}")],
    [KeyboardButton(text="Адмін Панель")]
])

admin_kbd = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f"Час прийому")],
    [KeyboardButton(text="Вийти з Адмін панелі")]
])
#Анкета
test_subj = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Українська мова', callback_data="ukr_philo"),
        InlineKeyboardButton(text='Українська література', callback_data="ukr_philo")
    ],
    [
        InlineKeyboardButton(text='Математика', callback_data="math"),
        InlineKeyboardButton(text='Фізика', callback_data="physics")
    ],
    [
        InlineKeyboardButton(text='Хімія', callback_data="chem-bio"),
        InlineKeyboardButton(text='Біологія', callback_data="chem-bio")
    ],
    [
        InlineKeyboardButton(text='Зарубіжна література', callback_data="foreign_philo")
    ],
    [
        InlineKeyboardButton(text='Інформатика', callback_data="it")
    ],
    [
        InlineKeyboardButton(text='Основи правознавства', callback_data='law')
    ]
])


skills = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Розв\'язання задач', callback_data="math"),
        InlineKeyboardButton(text='Робота з комп\'ютером', callback_data="it")
    ],
    [
        InlineKeyboardButton(text='Історичний аналіз', callback_data="history"),
        InlineKeyboardButton(text='Права та закони', callback_data="law")
    ],
    [
        InlineKeyboardButton(text='Природні науки', callback_data="geography"),
        InlineKeyboardButton(text='Дослідження природи', callback_data="chem_bio")
    ],
    [
        InlineKeyboardButton(text='Письмо та текст', callback_data="ukr_philo"),
        InlineKeyboardButton(text='Іноземні мови', callback_data="foreign_philo")
    ],
    [
        InlineKeyboardButton(text='Спорт', callback_data="sports_military"),
        InlineKeyboardButton(text='Творчість', callback_data="art")
    ]
])


develop_skills = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Логіка та обчислення', callback_data="math"),
        InlineKeyboardButton(text='Програмування', callback_data="it")
    ],
    [
        InlineKeyboardButton(text='Історичний аналіз', callback_data="history"),
        InlineKeyboardButton(text='Правознавство', callback_data="law")
    ],
    [
        InlineKeyboardButton(text='Географія та екологія', callback_data="geography"),
        InlineKeyboardButton(text='Хімічні дослідження', callback_data="chem_bio")
    ],
    [
        InlineKeyboardButton(text='Письмо та мовлення', callback_data="ukr_philo")],

    [InlineKeyboardButton(text='Культурологія та мови', callback_data="foreign_philo")],

    [
        InlineKeyboardButton(text='Спортивні навички', callback_data="sports_military"),
        InlineKeyboardButton(text='Художня творчість', callback_data="art")
    ]
])


favorite_tasks = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Аналітичні завдання', callback_data="math"),
        InlineKeyboardButton(text='Творчі проєкти', callback_data="art")
    ],
    [InlineKeyboardButton(text='Практичні експерименти', callback_data="chem_bio")],

    [InlineKeyboardButton(text='Написання текстів', callback_data="ukr_philology")],

    [
        InlineKeyboardButton(text='Вирішення логічних задач', callback_data="math")],
        [InlineKeyboardButton(text='Комунікація з людьми', callback_data="foreign_philo")
    ],
    [
        InlineKeyboardButton(text='Дослідження законів', callback_data="law")],
        [InlineKeyboardButton(text='Поглиблене вивчення історії', callback_data="history")
    ],
    [
        InlineKeyboardButton(text='Вивчення природних явищ', callback_data="geography")],
        [InlineKeyboardButton(text='Аналіз інформації', callback_data="it")
    ]
])



free_time = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Розв\'язую задачі', callback_data="math"),
        InlineKeyboardButton(text='Ігри / ІТ', callback_data="it")
    ],
    [
        InlineKeyboardButton(text='Історія / документалістика', callback_data="history"),
        InlineKeyboardButton(text='Читаю про права', callback_data="law")
    ],
    [
        InlineKeyboardButton(text='Природа / подорожі', callback_data="geography"),
        InlineKeyboardButton(text='Наукові дослідження', callback_data="chem_bio")
    ],
    [
        InlineKeyboardButton(text='Пишу тексти', callback_data="ukr_philo"),
        InlineKeyboardButton(text='Читаю іноземною', callback_data="foreign_philo")
    ],
    [
        InlineKeyboardButton(text='Займаюсь спортом', callback_data="sports_military"),
        InlineKeyboardButton(text='Малюю / музика', callback_data="art")
    ]
])


future_profession = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Математик / аналітик', callback_data="math"),
        InlineKeyboardButton(text='Програміст', callback_data="it")
    ],
    [
        InlineKeyboardButton(text='Історик', callback_data="historian"),
        InlineKeyboardButton(text='Юрист', callback_data="lawyer")
    ],
    [
        InlineKeyboardButton(text='Географ / еколог', callback_data="geography"),
        InlineKeyboardButton(text='Біолог / хімік', callback_data="bio_chem")
    ],
    [
        InlineKeyboardButton(text='Філолог (укр. мова)', callback_data="ukr_philo"),
        InlineKeyboardButton(text='Лінгвіст', callback_data="foreign_philo")
    ],
    [
        InlineKeyboardButton(text='Військовий / спортсмен', callback_data="sports_military")],
        [InlineKeyboardButton(text='Художник / дизайнер', callback_data="art")
    ]
])

#анкета закінчилась

socials_networks = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f"Наш Сайт {emoji.emojize(':globe_with_meridians:')}", url="http://tbl.km.ua/")],
    [InlineKeyboardButton(text=f'Сторінка у Facebook {emoji.emojize(':bust_in_silhouette::blue_book:')}', url='https://www.instagram.com/tbl_khm/')],
    [InlineKeyboardButton(text=f'Інстаграм {emoji.emojize(':camera:')}', url='https://www.instagram.com/tbl_khm/')],
    [InlineKeyboardButton(text=f'Телеграм Канал {emoji.emojize(':loudspeaker:')}', url='t.me/TBLLiveUA')]
])

profile_catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="◀️", callback_data="back"), InlineKeyboardButton(text="▶️", callback_data="next")],
    [InlineKeyboardButton(text=f"Дізнатися більше", url='http://tbl.km.ua/')]
])

about = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f'Дізнатись більше...', url='http://tbl.km.ua/')]
])