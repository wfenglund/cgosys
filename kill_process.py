import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # to make pygame import silent
import sys
import pygame
import subprocess

### Get the command line argument:
try:
    kill_button = int(sys.argv[1])
    flag = True
except:
    print('You need to supply a kill button id.')
    flag = False

### Initiate pygame and find controllers:
pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

### Functions:
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

### Loop:
while flag == True:
    joypress = get_contr_press()
    if joypress == kill_button:
        pidof_proc = subprocess.Popen(['pidof', 'vbam'], stdout = subprocess.PIPE)
        vbam_pid = pidof_proc.stdout.read().decode().replace('\n', '')
        if len(vbam_pid) > 0:
            subprocess.Popen(['kill', vbam_pid])
