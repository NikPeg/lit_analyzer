import asyncio
from audio_utils import transcoding_to_mp3
from ai_utils import GPTClient
from json_utils import Json_work
from yaspeech import Bucket_tools,  Speech_recognizer



class Multi_assistants_class:
    def __init__(self, gpt_token:str, gpt_model:str, gpt_voice_model:str,  asses:list, bucket_name:str, speech_secret_key:str):
        #gpt
        self.asses = asses
        self.g_t = gpt_token
        self.g_m = gpt_model
        self.g_v_m = gpt_voice_model

        self.J = Json_work()
        self.BT = Bucket_tools(speech_secret_key, bucket_name)
        self.SR = Speech_recognizer(speech_secret_key, bucket_name)

    #state 0 transcription    
    async def transcript(self, fp:str,  object_cloud_path:str) -> dict:
        
        await self.BT.object_upload(local_file_path=fp, object_path=object_cloud_path)

        flag = True

        up_file = self.J.read_l(await self.SR.audio_up(object_cloud_path))
        print(up_file['id'])
            
        t_g =''
        while flag != False:
            await asyncio.sleep(10)
            o_p = await self.SR.operation_get(up_file["id"])
            if self.J.read_l(o_p)['done'] == True: 
                flag = False
                t_g = await self.SR.transcript_get(up_file['id'])

            print(self.J.read_l(o_p)['done'])
        await self.SR.parse(t_g)
        return  {"text":await self.SR.parse(t_g), "state":0}
    
    async def asst2_complition(self,  data) -> dict:
        #state 1 - asst 3-2
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[0])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        answer = G_C.get_answer(tr)

        return {"text": answer, "state":1}
    
    async def asst3_complition(self,  data) -> dict:
        #state 1 - asst 3-3
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[1])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":2}
    
    async def asst4_complition(self,  data) -> dict:
        #state 2 - asst 3-4
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[2])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":3}
    
    async def asst5_complition(self,  data) -> dict:
        #state 1 - asst 3-5
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[2])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":4}
    
    async def asst6_complition(self,  data) -> dict:
        #state 1 - asst 3-6
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[3])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":5}
    
    async def asst7_complition(self,  data) -> dict:
        #state 1 - asst 3-7
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[4])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":6}
    
    async def asst8_complition(self,  data) -> dict:
        #state 1 - asst 3-8
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[5])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":7}
    
    async def asst9_complition(self,  data) -> dict:
        #state 1 - asst 3-9
        G_C = GPTClient(self.g_t, self.g_m, self.g_v_m, self.asses[6])
        tr= G_C.create_thread()
        G_C.add_message(tr, data)
        return {"text": G_C.get_answer(tr), "state":8}
    
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#MAC = Multi_assistants_class(asses=asses)
#asyncio.run(MAC.transcript( fp="C:\\Users\\13_14\\Desktop\\lit_analyzer\\test_audio\\aud4_isp.mp3"))