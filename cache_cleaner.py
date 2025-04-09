from pathlib import Path
from shutil import rmtree
import time
from config import cache_path, max_files

def cache_clean(cache_path:str=cache_path, max_files:int = max_files) ->bool:
    
    while(True):
        try:
            file_num = len([file for file in Path(cache_path).iterdir() if file.is_file()])
            if file_num >= max_files:
                rmtree(cache_path, ignore_errors=True)
                Path(cache_path).mkdir(parents=True, exist_ok=True)
            time.sleep(12)
        except ValueError:
            print(ValueError)
        

