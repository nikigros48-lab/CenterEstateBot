from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from forms.user import Form

router = Router()


def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть сайт", url="https://google.com")],
            [InlineKeyboardButton(text="What does the dog say", callback_data="whof")],
        ]
    )
    return keyboard


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Старт")],
            [KeyboardButton(text="Помощь"), KeyboardButton(text="О боте")]
        ],
        resize_keyboard=True
    )

    return keyboard


@router.callback_query(lambda c: c.data == "whof")
async def dog_say(callback: CallbackQuery):
    await callback.message.answer("Whof! Whof! Whof! Whof! Whof!")
    await callback.answer()


@router.message(Command("cancel"))
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкета отклонена")


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Заполнение анкеты. Введите своё имя")
    await state.set_state(Form.name)


@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer("Отлично! А теперь возраст:")
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом")
        return

    if 150 < int(message.text) < 18:
        await message.answer("К сожалению, такие сделки не проводятся")
        return

    await state.update_data(age=message.text)

    await message.answer("Отлично! А теперь email:")
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
async def process_email(message: Message, state: FSMContext):
    if "@" not in message.text or "." not in message.text:
        await message.answer("Email некорректный")
        return

    await state.update_data(email=message.text)

    data = await state.get_data()

    await message.answer(f"Отлично! Анкета готова: Имя - {data["name"]}, возраст - {data["age"]}, адрес электронной почты - {data["email"]}")
    await state.clear()


@router.message(F.photo)
async def process_photo(message: Message):
    photo = message.photo[-1]
    file_id = photo.file_id

    await message.answer(
        f"Вы отправили фото - ID photo <code>{file_id}</code>",
        parse_mode=ParseMode.HTML
    )

    await message.answer_photo(file_id, caption="Вот ваше фото")



#
# @router.message(Command("start"))
# @router.message(F.text.lower() == "старт")
# async def start(message: Message):
#     await message.answer(f"Здравствуйте, <b>{message.from_user.first_name or "Аноним"}</b>!", parse_mode="HTML", reply_markup=get_main_reply_keyboard())
#
# @router.message(Command("help"))
# async def help(message: Message):
#     await message.answer("Команды:\n/start - запустить бот\n/help - список команд\n/about - информация о боте", reply_markup=get_main_reply_keyboard())
#
@router.message(Command("about"))
@router.message(F.text.lower() == "о боте")
async def about(message: Message):
    await message.answer(f"Тут находится информация о боте. Твоё имя {message.from_user.first_name or "Аноним"}",  reply_markup=get_main_inline_keyboard())