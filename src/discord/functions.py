from random import randint
from os import system
from datetime import datetime
time = datetime.now()

def fadea(text):
    system(""); faded = ""
    blue = 100
    for line in text:
        faded += (f"\033[38;2;0;255;{blue}m{line}\033[0m")
        if not blue == 255:
            blue += 5
            if blue > 255:
                blue = 255
    return faded
                                         

def fade(text):
    system(""); faded = ""
    blue = 100
    for line in text.splitlines():
        faded += (f"\033[38;2;0;255;{blue}m{line}\033[0m\n")
        if not blue == 255:
            blue += 15
            if blue > 255:
                blue = 255
    return faded


def log(msg):
    with open("log.txt", "a") as file_object:
        file_object.write(f"{msg} | {time.hour}:{time.minute}:{time.second}\n")
        print(msg)