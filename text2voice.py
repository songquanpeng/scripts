import os

import pygame
import requests


def text2voice(text, lang=None, temp_file="./temp/temp.mp3"):
    os.makedirs(os.path.dirname(temp_file), exist_ok=True)
    if len(text) == 0:
        return
    if lang is None:
        if '\u4e00' <= text[0] <= '\u9fa5':
            lang = 'cn'
    if lang == 'cn':
        tts_url = "https://tts.baidu.com/text2audio?lan=zh&ie=UTF-8&spd=5&text="
    else:
        tts_url = "https://dict.youdao.com/dictvoice?type=1&audio=`"
    r = requests.get(f"{tts_url}{text}")
    with open(temp_file, "wb") as f:
        f.write(r.content)
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.unload()
    os.remove(temp_file)


if __name__ == '__main__':
    text2voice("测试中文")
    text2voice("Test English")
