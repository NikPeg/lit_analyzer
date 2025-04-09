from openai import OpenAI
from pathlib import Path
import base64
import time
import tiktoken

encoding = tiktoken.encoding_for_model('gpt-4o')

class GPTClient:
    def __init__(self, token: str, model: str, voice_model:str, assist_id: str):
        self.token = token
        self.client = OpenAI(api_key=self.token)
        self.model = model
        self.voice_model = voice_model
        self.assist_id = assist_id


    def upload_file(self, path:str) -> str:
        result = self.client.files.create(
            file=Path(path),
            purpose="assistants",
        )
        return result.id
    
    ######################
    def create_assistant(self, name:str, instructions:str, file_paths:str) -> str:
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            instructions=instructions,
            tools=[{"type": "file_search"}],           
        )

        file_streams = [Path(path) for path in file_paths]
        vector_store = self.client.beta.vector_stores.create(name="Content plan ref")
        file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id, files=file_streams
        )
        print(file_batch.status)
        print(file_batch.file_counts)

        assistant = self.client.beta.assistants.update(
                assistant_id=assistant.id,
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
        )

        print("assistant_id:", assistant.id, "vector_store_id:", vector_store.id)
        return [assistant.id, vector_store.id]

    def create_assistant_without_files(self, name:str, instructions:str) -> str:
        assistant = self.client.beta.assistants.create(
            model=self.model,
            name=name,
            instructions=instructions,
        )

        print("assistant_id:", assistant.id)
        return assistant.id
    ######################
    def create_thread(self) -> str:
        thread = self.client.beta.threads.create(timeout=15)
  
        return thread.id
    
    def delete_thread(self, thread_id:str) -> str:
        deleted_thread =  self.client.beta.threads.delete(thread_id)
        print(deleted_thread)
        return deleted_thread
    
    def upload_file(self, path:str, purpose="assistants"):
        result = self.client.files.create(
            file=open(path, "rb"),
            purpose=purpose,
        )
        return result.id
    
    def add_message(self, thread_id:str, user_question:str, file_id:str=None) -> str:
        if file_id != None:
            message =  self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content= user_question,
                attachments= [{"file_id":file_id,  "tools": [{"type": "file_search"}]}]
            )
            return message
        else:
             message =  self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content= user_question
            )
             return message
        
    def add_message_without_thread(self, user_question:str, file_id:str=None) ->str:
        if file_id != None:
            message = self.client.chat.completions.create
            
        
    def add_audio(self, audio:base64, text_resp:str) -> str:
        encoded_string = base64.b64encode(open(audio, "rb").read())
        audio_add = self.client.chat.completions.create(
            model= self.voice_model,
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "mp3"},
            messages=[
                        {
                            "role": "user",
                            "content": [
                                { 
                                    "type": "text",
                                    "text": text_resp
                                },
                                {
                                    "type": "input_audio",
                                    "input_audio": {
                                        "data": encoded_string.decode('utf-8'),
                                        "format": "mp3"
                                    }
                                }
                            ]
                            },
            ]
        )
        return(audio_add.choices[0].message.audio.transcript)
    
    def get_answer(self, thread_id:str) -> str:
        run =  self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assist_id,
        )
        while True:
            run_info =  self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_info.completed_at:
                break
            time.sleep(1)
        messages = self.client.beta.threads.messages.list(thread_id)
        assistant_messages = []
        tokens_count = 0
        for message_data in messages.data:
            if message_data.role == "assistant":
                text_content = message_data.content[0].text.value
                tokens = encoding.encode(text_content)
                tokens_count += len(tokens)
                assistant_messages.append(message_data.content[0].text.value)
            else:
                break
        return "".join(assistant_messages[::-1])
    
