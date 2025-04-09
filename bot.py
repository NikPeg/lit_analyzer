import asyncio
import threading

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

from aiogram.client.telegram import TelegramAPIServer 
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer 




import os
from cache_cleaner import cache_clean

from audio_utils import transcoding_to_mp3
from json_utils import Json_work
from ai_utils import GPTClient
from mongo_utils import DBClient
from yaspeech import Bucket_tools,  Speech_recognizer
from multi_assitants_utils import Multi_assistants_class

from config import*

from templates.keyboards import keyboard_fast,  keyboard_main, keyboard_states_done, keyboard_states_process

J= Json_work()
GPT = GPTClient(gpt_token, gpt_model, gpt_voice_model, assist_id)
DB = DBClient(mongo_client_ref, db_name)

BT = Bucket_tools(speech_token, bucket_name)
SR = Speech_recognizer(speech_secret_key, bucket_name)
bot_templates_path = {"keyboard":os.path.join("templates", "keyboards_temp.json"), "messages":os.path.join("templates", "msg_temp.json")}

logging.basicConfig(level=logging.INFO)

threading.Thread(target=cache_clean).start()
logging.info(f"thread {cache_clean.__name__} is starting")

MAC =Multi_assistants_class(gpt_token, gpt_model, gpt_voice_model, asses, bucket_name, speech_secret_key)

session = AiohttpSession(api=TelegramAPIServer.from_base("http://localhost:8081", is_local=True))
bot = Bot(token=bot_token, session=session)

dp = Dispatcher()

def id_check(msg_id:int):
   DB_id = DB.find(collection_name, False, {"tg_id":msg_id})
   if DB_id == None:
    query ={"tg_id":msg_id,  "state":None, "text": None, "asst3_answer": None, "asst4_answer":None, "asstn_answer":None}
    return DB.insert(collection_name, dict(query), False)          


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    id_check(message.from_user.id)

    await message.answer(J.read_p(path=bot_templates_path["messages"])["start"], reply_markup=keyboard_main)

    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)


@dp.message()
async def GPT_data_handler(message: types.Message):
    id_check(message.from_user.id)

    if message.audio and message.chat.id != reply_chat_id or message.document and message.chat.id != reply_chat_id or message.voice and message.chat.id != reply_chat_id:
        #logging.INFO("messge_type: audio or document" )
        file = None
        if message.audio:
            file=await bot.get_file(message.audio.file_id)
        elif message.voice:
            file=  file=await bot.get_file(message.voice.file_id)
        else:
            file =await bot.get_file(message.document.file_id)
        print(file)  
        strp = file.file_path.split(".")

        print(strp[1])
        if strp[1] in ('mp3', 'mp4', 'wav', 'ogg', 'oga', 'mkv', 'm4a'):
            #transcription
            downloaded_file = await bot.download_file(file.file_path)
            fp=os.path.join(cache_path, f"doc_{message.from_user.id}.{strp[1]}")
            print(fp)

            open(fp, 'wb').write(downloaded_file.read())
            trans = None
            if strp[1] == "mp3":
                trans = await MAC.transcript(fp, object_cloud_path)
            else:
                trans = await MAC.transcript(await transcoding_to_mp3(fp), object_cloud_path)
            text = "стейт: "+str(trans["state"]) +"\n" +trans["text"]
            print(len(text))
            if len(text) > max_symb_in_msg:
                    for x in range(0, len(text), max_symb_in_msg):
                        
                        mess = text[x: x + max_symb_in_msg]         
                        await message.answer(mess, reply_markup=keyboard_states_done)

                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)
                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+2)
            else:
                await message.answer(text, reply_markup=keyboard_main) 

                await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
                await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)

            DB.update(collection_name, {"tg_id": message.from_user.id}, {"$set":{"text": trans["text"], "state":trans["state"]}})
        
        else:
            await message.answer(J.read_p(bot_templates_path["messages"])["error_not_support_file"])
            await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
            await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)

    if message.text == "Продолжить":
        user_in_db = DB.find(collection=collection_name, all=False, query={"tg_id":message.from_user.id})

        
        text = None
        answer = None

        match user_in_db["state"]:
            case 0:
                #text correct asst
                answer= await MAC.asst2_complition(user_in_db["text"])
                DB.update(collection_name, {"tg_id": message.from_user.id}, {"$set":{"text": answer["text"], "state":answer["state"]}})         
                text = "стейт: "+str(answer["state"]) +"\n" +answer["text"]

            case 1:
                #analyzer
                answer = await MAC.asst3_complition(user_in_db["text"])
                text = "стейт: "+str(answer["state"]) +"\n" +answer["text"]
                DB.update(collection_name, {"tg_id": message.from_user.id}, {"$set":{"asst3_answer": answer["text"], "state":answer["state"]}})

            case 2:
                #struct
                template ="*Исходный текст* \n" + str(user_in_db["text"]) + " \n *Результат работы ассистента:* \n" + str(user_in_db["asst3_answer"])
                answer = await MAC.asst4_complition(template)
                text = "стейт: "+str(answer["state"]) +"\n" +answer["text"]
                DB.update(collection_name, {"tg_id": message.from_user.id}, {"$set":{"asst4_answer": answer["text"], "state":answer["state"]}})

            case 3:
                #lit_analyzer
                template ="*Исходный текст* \n" + str(user_in_db["text"]) + "\n *Результат работы преведущего ассистента*"+ str(user_in_db["asst3_answer"])+ "\n  *Результат работы ассистента:* \n" + str(user_in_db["asst_answer4"])
                answer = await MAC.asst5_complition(template)
                text = "стейт: "+str(answer["state"]) +"\n" +answer["text"]
                DB.update(collection_name, {"tg_id": message.from_user.id}, {"$set":{"asst_answer5": answer["text"], "state":answer["state"]}})

            case _:
                  DB.delete(collection_name , {"tg_id":message.from_user.id,  "state":None, "text": None, "asst3_answer": None, "asst4_answer":None, "asstn_answer":None}, True)
                  text=J.read_p(bot_templates_path["messages"])["error_state_not_found"]                 

             
        if len(text) > max_symb_in_msg:
                    for x in range(0, len(text), max_symb_in_msg):

                        mess = text[x: x + max_symb_in_msg]         
                        await message.answer(mess, reply_markup=keyboard_states_done)
                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)
                    await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+2)
        else:
                await message.answer(text, reply_markup=keyboard_states_done)
                await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id)
                await bot.forward_message(chat_id= reply_chat_id, from_chat_id=message.chat.id, message_id=message.message_id+1)

        


asyncio.run(dp.start_polling(bot))