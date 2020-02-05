import pygame
import time
import msvcrt


def sound_play():
    while True:
        pygame.mixer.init()
        pygame.mixer.music.load("sa.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() and not msvcrt.kbhit():
            time.sleep(0.1)
        pygame.mixer.music.stop()
        if msvcrt.kbhit():
            while msvcrt.kbhit():
                s = msvcrt.getch()
            break


if __name__ == '__main__':
    sound_play()