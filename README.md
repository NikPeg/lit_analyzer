Создайте виртуальное окружение  
Установите зависимости pip install -r requirements.txt  
Поднимите telegram-bot-api, если нужна расшифровка длинных лекций (от часа)  
Запустите python3 nb.py  
Формат файла config.py:  
```
#TG
bot_token = ""
cache_path = "cache"
max_files =  6
admin_ids = []
reply_chat_id = 0
max_symb_in_msg = 4095

#gpt
gpt_token = "sk-"
gpt_model = "gpt-4o"
gpt_voice_model = "gpt-4o-audio-preview"
vector_store_id = "vs_"
assist_id = "asst_"
asses = [
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    "asst_",
    ]
ass_name = [
    "предварительной обработки текста",
    "анализа содержания",
    "cтруктурирования сценария",
    "литературной обработки",
    "aдаптации к целевой аудитории",
    "редактуры и корректуры",
    "формирования методики",
    "написания введения",
    "написания заключения",
]
MAX_DURATION = 30
#yandex
speech_token =""
speech_secret_key = ""
bucket_name = ""
object_cloud_path = f"{bucket_name}/audio.mp3"

#DB
mongo_client_ref = "mongodb+srv:"
db_name = ""
collection_name =""
```
