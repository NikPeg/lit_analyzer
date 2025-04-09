from ffmpeg.asyncio import FFmpeg
from config import cache_path
import os
async def transcoding_to_mp3(file_path:str, output_name:str=os.path.join(cache_path, "output.mp3")):
    ffmpeg = (
        FFmpeg()
        .option("y")
        .input(file_path)
        .output(
            output_name,
            **{'q:a': 0}
        )
    )

    await ffmpeg.execute()
    return output_name

