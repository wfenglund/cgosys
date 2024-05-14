### Packages:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # to make pygame import silent
import pygame
import subprocess
import curses

### Initiate pygame find controllers:
pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

### Functions:
def detect_games(rom_path, game_type, ending):
    file_list = os.listdir(rom_path)
    game_dict = {}
    game_dict[game_type] = [i for i in file_list if i.endswith(ending)]
    return game_dict

def get_contr_press():
    if len(controllers) > 0:
        controllers[0].init()
        button_dict = {12:258, 11:259, 0:10, 7:7}
        events = pygame.event.get()
        if len(events) > 0:
            for press in events:
                if 'button' in press.dict.keys():
                    button = press.dict['button']
                    button = button_dict[button] if button in button_dict.keys() else ''
                    controllers[0].quit()
                    return button
    return ''

def cgosys_menu(stdscr):
    stdscr.nodelay(True) # do not for .getch()
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['normal'] = curses.color_pair(1)
    attributes['highlighted'] = curses.color_pair(2)
    while True:
        character = 0  # last character read
        option = 0  # the current option that is marked
        choices = roms['gba'] + ['Quit']
        while character != 10: # while Enter has not been pressed
            stdscr.erase()
            stdscr.addstr("Select game to play:\n", curses.A_UNDERLINE)
            for i in range(len(choices)): # paint menu choices
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                stdscr.addstr(choices[i] + '\n', attr)
            character = stdscr.getch()
            if character == -1: # if no key was pressed
                joypress = get_contr_press()
                if joypress != '': # if controller has been pressed
                    character = joypress
            if character == curses.KEY_UP and option > 0:
                option -= 1
            elif character == curses.KEY_DOWN and option < len(choices) - 1:
                option += 1
        choice = choices[option] # get menu choice
        if choice == 'Quit':
            break
        else:
            message = f'Running {choice}...'
            print(message, end = '\r')
            devnull = subprocess.DEVNULL
            subprocess.run(['vbam', '-c', device_config, f'{gba_roms_path}{choice}'], stdout = devnull, stderr = devnull)
            print(' ' * len(message), end = '\r') # clean avay message

### Determine VBAM settings:
device = 'PowerA'
# device = 'keyboard'

config_dict = {}
config_dict['PowerA'] = 'powera_vbam.cfg'
config_dict['keyboard'] = 'keyboard_vbam.cfg'

device_config = config_dict[device]

### Detect GBA games:
gba_roms_path = './gba_roms/'
roms = detect_games(gba_roms_path, 'gba', '.gba')

### Spawn subprocess for quitting VBAM from within, and start cgosys menu:
kill_proc = subprocess.Popen(['python3', './kill_process.py'])
curses.wrapper(cgosys_menu)
kill_proc.kill()
