import aiohttp
import asyncio
from config import speech_secret_key, speech_token, bucket_name
import json

#out="https://stt.api.cloud.yandex.net/stt/v3/getRecognition" #+"<operation_id>"


class Bucket_tools:
    def __init__(self, api_key:str,  bucket_name:str):
        self.api_key = api_key
        self.bucket_name = bucket_name
    async def object_upload(self, object_path:str, local_file_path:str)->str: #object path - path in bucket to object
        request = f"https://storage.yandexcloud.net/{self.bucket_name}/{object_path}"
        headers = {
                    'Authorization': f'Api-key {self.api_key}',
                    'Content-Type': 'application/octet-stream',
        }
        encoded_data = open(local_file_path, "rb").read()
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.put(request, data=encoded_data)
            return await response.text()

    async def object_get(self, object_path:str)->str:
        request = f"https://storage.yandexcloud.net/{self.bucket_name}/{object_path}"
        headers = {
                    'Authorization': f'Api-key {self.api_key}',
                    'Content-Type': 'application/octet-stream',
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            response = await session.get(request)
            return await response.text()


class Speech_recognizer:
    def __init__(self, api_key: str, bucket_name: str):
        self.api_key = api_key
        self.bucket_name = bucket_name

    async def audio_up(self, bucket_aud_name: str) -> dict:
        url =  "https://stt.api.cloud.yandex.net/stt/v3/recognizeFileAsync"
        request = {
                    "uri": f"https://storage.yandexcloud.net/{self.bucket_name}/{bucket_aud_name}",
                    "recognitionModel": {
                    "model": "general",
                    "audioFormat": {
                        "containerAudio": {
                                    "containerAudioType": "MP3"
                    }
                }
            }
        }

        headers = {
            'Authorization': f'Api-key {self.api_key}',
            'Content-Type': 'application/json'
        }
        print(request)
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=request, headers=headers) as response:
                return await response.json()

    async def operation_get(self, operation_id: str) -> dict:
        url =  f"https://operation.api.cloud.yandex.net/operations/{operation_id}"
        headers = {
            'Authorization': f'Api-key {self.api_key}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.json()

    async def transcript_get(self, operation_id: str) -> dict:
        url =  f"https://stt.api.cloud.yandex.net/stt/v3/getRecognition?operationId={operation_id}"
        headers = {
            'Authorization': f'Api-key {self.api_key}',
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                return await response.text()
            
    async def parse(self, resp):
        # Разбиваем строку на отдельные JSON-объекты
        json_objects = resp.strip().split('\n')

        # Список для хранения всех объединенных текстов из каждого JSON-объекта
        all_concatenated_texts = []
        for json_object in json_objects:
            try:
                data = json.loads(json_object)
                # Проверяем, существует ли ключ "final" в данном JSON-объекте
                if "final" in data['result']:
                    concatenated_text = ' '.join(
                        word['text'] for word in data['result']['final']['alternatives'][0]['words']
                    )
                    all_concatenated_texts.append(concatenated_text)
            except json.JSONDecodeError:
                pass  # Игнорируем ошибки декодирования JSON
            except KeyError:
                pass  # Игнорируем ошибки ключей

        # Выводим каждый объединенный текст из отдельных JSON-объектов
        res=''
        for text in all_concatenated_texts:
            res +=text
        return res  

"""bt = Bucket_tools(speech_token, bucket_name)

sr = Speech_recognizer(speech_secret_key, bucket_name)
res = ''

async def rn():

    while res != "done":
        id= (await sr.audio_up("audio%2Faud.mp3")["id"])
        print(id)
        await asyncio.sleep(120)
        res = (await sr.transcript_get(id)["done"])

#print(asyncio.run(sr.audio_up("audio%2Faud.mp3")))

result = asyncio.run(sr.transcript_get("f8dk7u1kmhrnpm6nfh1i"))"""
