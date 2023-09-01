import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
import subprocess
import edge_tts

from shortGPT.audio.voice_module import VoiceModule
from shortGPT.config.languages import (EDGE_TTS_VOICENAME_MAPPING,
                                       LANGUAGE_ACRONYM_MAPPING, Language)
from shortGPT.subtitles.subtitles_utls import add_punctuation_to_srt

def run_async_func(loop, func):
    return loop.run_until_complete(func)


class EdgeTTSVoiceModule(VoiceModule):
    def __init__(self, voiceName):
        self.voiceName = voiceName
        super().__init__()

    def update_usage(self):
        return None

    def get_remaining_characters(self):
        return 999999999999

    def generate_voice(self, text, outputfile, captionsfile=None):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            with ThreadPoolExecutor() as executor:
                loop.run_in_executor(executor, run_async_func, loop, self.async_generate_voice(text, outputfile, captionsfile))

        finally:
            loop.close()
        if not os.path.exists(outputfile):
            print("An error happened during edge_tts audio generation, no output audio generated")
            raise Exception("An error happened during edge_tts audio generation, no output audio generated")
        return outputfile

    async def async_generate_voice(self, text, outputfile, captionsfile=None):
        try:
            communicate = edge_tts.Communicate(text, self.voiceName)
            submaker = edge_tts.SubMaker()
            with open(outputfile, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
            webvtt_file = os.path.splitext(outputfile if not captionsfile else captionsfile)[0]+".vtt"
            srt_file = os.path.splitext(webvtt_file)[0]+".srt"
            with open(webvtt_file, "w", encoding="utf-8") as file:
                file.write(submaker.generate_subs())
            subprocess.run(['ffmpeg', '-i', webvtt_file, srt_file])
            if os.path.exists(srt_file):
                with open(srt_file, "r", encoding="utf-8") as file:
                    original_srt = file.read()
                new_srt = add_punctuation_to_srt(original_srt, text)
                with open(srt_file, "w", encoding="utf-8") as file:
                    file.write(new_srt)
        except Exception as e:
            print("Error generating audio using edge_tts", e)
            raise Exception("An error happened during edge_tts audio generation, no output audio generated", e)
        return outputfile
