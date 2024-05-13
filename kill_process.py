import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # to make pygame import silent
import pygame
import subprocess

pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

def get_contr_press():
    if len(controllers) > 0:
        controllers[0].init()
        events = pygame.event.get()
        if len(events) > 0:
            for press in events:
                if 'button' in press.dict.keys():
                    button = press.dict['button']
                    controllers[0].quit()
                    return button
    return ''

while True:
    joypress = get_contr_press()
    if joypress == 7:
        pidof_proc = subprocess.Popen(['pidof', 'vbam'], stdout = subprocess.PIPE)
        vbam_pid = pidof_proc.stdout.read().decode().replace('\n', '')
        if len(vbam_pid) > 0:
            subprocess.Popen(['kill', vbam_pid])
