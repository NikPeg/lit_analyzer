import asyncio
import threading

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import os

from cache_cleaner import cache_clean
from audio_utils import transcoding_to_mp3
from json_utils import Json_work
from ai_utils import GPTClient
from mongo_utils import DBClient

from config import *


GPT = GPTClient(gpt_token, gpt_model, gpt_voice_model, None)

asses = []
line = ''
while line != 'СТОП':
    print("Введите имя ассистента")
    name = input()
    print("Введите промпт")
    line = ""
    prompt = ""
    while line != "stop" and line != "стоп" and line != "СТОП":
        prompt += line + "\n"
        line = input()
    asses.append(GPT.create_assistant_without_files(name, prompt))

print(asses)
