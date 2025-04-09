from aiogram import  types
from json_utils import Json_work
import os
Json_work = Json_work()
bot_templates_path = os.path.join("templates", "keyboards_temp.json")
kb = [
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["fast_answer"])],
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["reply"])],
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["help"])]
    ]
kb_states_done =[
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["cont"])],
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["stop"])],
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["help"])]
    ]
kb_states_process =[
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["stop"])],
        [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["help"])]
    ]
kb_fast = [
            [types.KeyboardButton(text=Json_work.read_p(bot_templates_path)["help"])]
]
keyboard_main = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=Json_work.read_p(bot_templates_path)["placeholder"]
    )

keyboard_states_done = types.ReplyKeyboardMarkup(
        keyboard=kb_states_done,
        resize_keyboard=True,
        input_field_placeholder=Json_work.read_p(bot_templates_path)["placeholder_states"]
    )
keyboard_states_process = types.ReplyKeyboardMarkup(
        keyboard=kb_states_done,
        resize_keyboard=True,
        input_field_placeholder=Json_work.read_p(bot_templates_path)["placeholder_states"]
    )
keyboard_fast = types.ReplyKeyboardMarkup(
     keyboard=kb_fast,
     resize_keyboard=True,
    input_field_placeholder=Json_work.read_p(bot_templates_path)["fast_answer_placeholder"]
)

kb_start = [
    [types.KeyboardButton(text="Доп. информация")],
    [types.KeyboardButton(text="Оркестр ассистентов")],
    [types.KeyboardButton(text="Введение"), types.KeyboardButton(text="Заключение"), types.KeyboardButton(text="Методика")],
]
keyboard_start = types.ReplyKeyboardMarkup(
    keyboard=kb_start,
    resize_keyboard=True,
    input_field_placeholder=Json_work.read_p(bot_templates_path)["fast_answer_placeholder"]
)

kb_continue = [
    [types.KeyboardButton(text="Продолжить")],
    [types.KeyboardButton(text="Заново")],
    [types.KeyboardButton(text="Сформировать документ")]
]
keyboard_continue = types.ReplyKeyboardMarkup(
    keyboard=kb_continue,
    resize_keyboard=True,
    placeholder_states=Json_work.read_p(bot_templates_path)["continue_answer_placeholder"]
)

no_keyboard = types.ReplyKeyboardRemove()

kb_band = [
    [types.KeyboardButton(text="Использовать оркестр")],
    [types.KeyboardButton(text="Без оркестра")]
]
keyboard_band = types.ReplyKeyboardMarkup(
    keyboard=kb_band,
    resize_keyboard=True,
    placeholder_states="Выберите способ взаимодействия с ботом"
)
