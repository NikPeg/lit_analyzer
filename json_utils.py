import json
import codecs
class Json_work:
    def __init__(self):
          pass
    
    def read_p(self, path:str) -> str:
        with codecs.open(path, "r",  "utf_8_sig") as f:
                file_content = f.read()
                templates = json.loads(file_content)
                return(templates)
    def read_l(self, obj:str)-> str:
          s1 = json.dumps(obj)
          return json.loads(s1)


