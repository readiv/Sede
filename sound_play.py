import pygame
import time


def sound_play():
    try:
        while True:
            pygame.mixer.init()
            pygame.mixer.music.load("sa.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(1)
            pygame.mixer.music.stop()
    except KeyboardInterrupt:
        pass
