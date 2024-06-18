### Packages:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # to make pygame import silent
import pygame
import time
import subprocess
import curses
import re

### Find cgosys path:
cgosys_path = os.path.dirname(__file__)

### Initiate pygame and find controllers:
pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

### Determine controller and which settings to use:
controller_dict = {}
controller_dict['0'] = 'keyboard'
controller_dict['1'] = 'PowerA_1'
controller_dict['2'] = 'PowerA_2'

try:
    settings_choice = int(sys.argv[1])
    device = controller_dict[settings_choice]
except:
    print('You need to set controller, possible alternatives:')
    print('0: Keyboard')
    print('1: PowerA 1')
    print('2: PowerA 2')
    settings_choice = input('Choose a number: ')
    device = controller_dict[settings_choice]

### Functions:
def title_prompt(stdscr):
    prompt_x = (curses.COLS // 2) - (60 // 2)
    stdscr.addstr(0, prompt_x, r" ________  ________  ________  ________  __    __  ________ ")
    stdscr.addstr(1, prompt_x, r"/       /|/       /|/       /|/       /|/ /|  / /|/       /|")
    stdscr.addstr(2, prompt_x, r"$$$$$$$$/ $$$$$$$$ |$$$$$$$$ |$$$$$$$$/ $$ |  $$ |$$$$$$$$/ ")
    stdscr.addstr(3, prompt_x, r"$$ |      $$ |  $$ |$$ |  $$ |$$/     /|$$ |  $$ |$$/     /|")
    stdscr.addstr(4, prompt_x, r"$$ |_____ $$ |__$$ |$$ |__$$ |$$$$$$$$ |$$ |__$$ |$$$$$$$$ |")
    stdscr.addstr(5, prompt_x, r"$$/     /|$$/   $$ |$$/   $$ |/     $$ |$$/   $$ |/     $$ |")
    stdscr.addstr(6, prompt_x, r"$$$$$$$$/ $$$$$$$$ |$$$$$$$$/ $$$$$$$$/ $$$$$$$$ |$$$$$$$$/ ")
    stdscr.addstr(7, prompt_x, r"          / /|__$$ |                    / /|__$$ |          ")
    stdscr.addstr(8, prompt_x, r"          $$/   $$ |   casual  gaming   $$/   $$ |          ")
    stdscr.addstr(9, prompt_x, r"          $$$$$$$$/   operating system  $$$$$$$$/          ")

def detect_games(rom_path, ending):
    if os.path.isdir(rom_path):
        file_list = os.listdir(rom_path)
    else:
        file_list = []
    game_list = [i for i in file_list if i.endswith(ending)]
    return game_list

def get_contr_press():
    press = ''
    if len(controllers) > 0:
        controllers[0].init()
        button_dict = {12:258, 11:259, 0:10, 2:10, 7:7, (0, -1):258, (0, 1):259}
        events = pygame.event.get()
        if len(events) > 0:
            for entry in events:
                if 'button' in entry.dict.keys():
                    press = entry.dict['button']
                if 'hat' in entry.dict.keys():
                    press = entry.dict['value']
                press = button_dict[press] if press in button_dict.keys() else ''
                time.sleep(0.15)
        controllers[0].quit()
    return press

def cgosys_menu(stdscr):
    stdscr.nodelay(True) # do not wait for .getch()
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['normal'] = curses.color_pair(1)
    attributes['highlighted'] = curses.color_pair(2)
    while True:
        character = 0  # last character read
        option = 0  # the current option that is marked
        choices = list(console_dict.keys()) + ['Quit']
        while character != 10: # while Enter has not been pressed
            stdscr.erase()
            # Add prompt and menu title:
            title_prompt(stdscr)
            title_str = "SELECT CONSOLE\n"
            title_y = 11
            title_x = (curses.COLS // 2) - (len(title_str) // 2)
            stdscr.addstr(title_y, title_x, title_str, curses.A_UNDERLINE)
            # Add menu options:
            line_n = title_y + 2
            for i in range(len(choices)):
                col_w = 30
                cur_opt = choices[i]
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                option_x = (curses.COLS // 2) - (col_w // 2)
                opt_list = re.findall('.{1,' + str(col_w) + '}', cur_opt)
                for chunk in opt_list:
                    nchar = len(chunk)
                    chunk = chunk if nchar == col_w else chunk + ' '*(col_w - nchar)
                    stdscr.addstr(line_n, option_x, chunk + '\n', attr)
                    line_n = line_n + 1
            # Get user input:
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
            return 'shutdown'
        else:
            console_info = console_dict[choice]
            return curses.wrapper(cgosys_console, console_info)

def cgosys_console(stdscr, console_info):
    stdscr.nodelay(True) # do not wait for .getch()
    roms = detect_games(console_info[0], console_info[1])
    attributes = {}
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    attributes['normal'] = curses.color_pair(1)
    attributes['highlighted'] = curses.color_pair(2)
    while True:
        character = 0  # last character read
        option = 0  # the current option that is marked
        choices = roms + ['Quit']
        while character != 10: # while Enter has not been pressed
            stdscr.erase()
            # Add prompt and menu title:
            title_prompt(stdscr)
            title_str = "SELECT ROM\n"
            title_y = 11
            title_x = (curses.COLS // 2) - (len(title_str) // 2)
            stdscr.addstr(title_y, title_x, title_str, curses.A_UNDERLINE)
            # Add menu options:
            line_n = title_y + 2
            for i in range(len(choices)):
                col_w = 36
                cur_opt = choices[i]
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                option_x = (curses.COLS // 2) - (col_w // 2)
                opt_list = re.findall('.{1,' + str(col_w) + '}', cur_opt)
                for chunk in opt_list:
                    nchar = len(chunk)
                    chunk = chunk if nchar == col_w else chunk + ' '*(col_w - nchar)
                    stdscr.addstr(line_n, option_x, chunk + '\n', attr)
                    line_n = line_n + 1
            # Get user input:
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
            option = 0
            return curses.wrapper(cgosys_menu)
        else:
            message = f'Running {choice}...'
            print(message, end = '\r')
            devnull = subprocess.DEVNULL
            subprocess.run(['vbam', '-c', device_config, f'{console_info[0]}{choice}'], stdout = devnull, stderr = devnull)
            print(' ' * len(message), end = '\r') # clean away message

### Determine VBAM settings:
config_dict = {}
config_dict['PowerA_1'] = [cgosys_path + '/powera_vbam.cfg', 7]
config_dict['PowerA_2'] = [cgosys_path + '/powera_vbam_2.cfg', 10]
config_dict['keyboard'] = [cgosys_path + '/keyboard_vbam.cfg', 1000]

device_config = config_dict[device][0]

### Detect GBA games:
if os.path.isdir(os.getenv("HOME") + '/Rom_files'):
    location = os.getenv("HOME")
else:
    location = '.'
console_dict = {}
console_dict['Gameboy Original'] = [location + '/Rom_files/gb_roms/', '.gb']
console_dict['Gameboy Color'] = [location + '/Rom_files/gbc_roms/', '.gbc']
console_dict['Gameboy Advance'] = [location + '/Rom_files/gba_roms/', '.gba']

### Spawn subprocess for quitting VBAM from within, and start cgosys menu:
kill_script = cgosys_path + '/kill_process.py'
kill_button = str(config_dict[device][1])
kill_proc = subprocess.Popen(['python3', kill_script, kill_button])
curses.wrapper(cgosys_menu)
kill_proc.kill()
