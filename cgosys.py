### Packages:
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # to make pygame import silent
import pygame
import subprocess
import curses

### Initiate pygame and find controllers:
pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

### Functions:
def detect_games(rom_path, game_type, ending):
    file_list = os.listdir(rom_path)
    game_list = [i for i in file_list if i.endswith(ending)]
    return game_list

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
            # Add menu title:
            title_str = "Select console:\n"
            title_y = 1
            title_x = (curses.COLS // 2) - (len(title_str) // 2)
            stdscr.addstr(title_y, title_x, title_str, curses.A_UNDERLINE)
            # Add menu options:
            line_n = 2
            for i in range(len(choices)):
                extra_space = 0
                cur_opt = choices[i]
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                option_x = (curses.COLS // 2) - (30 // 2)
                if len(cur_opt) > 30:
                    cur_opt = cur_opt[0:30] + '\n' + ' '*option_x + cur_opt[30:] + ' '*(30 - len(cur_opt[30:]))
                    extra_space = 1
                else:
                    cur_opt = cur_opt + ' '*(30 - len(cur_opt))
                cur_opt = ' '*option_x + cur_opt
                stdscr.addstr(line_n, 0, cur_opt + '\n', attr)
                line_n = line_n + 1 + extra_space
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
            break
        else:
            console_info = console_dict[choice]
            return curses.wrapper(cgosys_console, console_info)

def cgosys_console(stdscr, console_info):
    stdscr.nodelay(True) # do not wait for .getch()
    roms = detect_games(console_info[0], console_info[1], console_info[2])
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
            # Add menu title:
            title_str = "Select game to play:\n"
            title_y = 1
            title_x = (curses.COLS // 2) - (len(title_str) // 2)
            stdscr.addstr(title_y, title_x, title_str, curses.A_UNDERLINE)
            # Add menu options:
            line_n = 2
            for i in range(len(choices)):
                extra_space = 0
                cur_opt = choices[i]
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                option_x = (curses.COLS // 2) - (30 // 2)
                if len(cur_opt) > 30:
                    cur_opt = cur_opt[0:30] + '\n' + ' '*option_x + cur_opt[30:] + ' '*(30 - len(cur_opt[30:]))
                    extra_space = 1
                else:
                    cur_opt = cur_opt + ' '*(30 - len(cur_opt))
                cur_opt = ' '*option_x + cur_opt
                stdscr.addstr(line_n, 0, cur_opt + '\n', attr)
                line_n = line_n + 1 + extra_space
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
device = 'PowerA'
# device = 'keyboard'

config_dict = {}
config_dict['PowerA'] = 'powera_vbam.cfg'
config_dict['keyboard'] = 'keyboard_vbam.cfg'

device_config = config_dict[device]

### Detect GBA games:
console_dict = {}
console_dict['Gameboy Original'] = ['./gb_roms/', 'gb', '.gb']
console_dict['Gameboy Color'] = ['./gbc_roms/', 'gbc', '.gbc']
console_dict['Gameboy Advance'] = ['./gba_roms/', 'gba', '.gba']

### Spawn subprocess for quitting VBAM from within, and start cgosys menu:
kill_proc = subprocess.Popen(['python3', './kill_process.py'])
curses.wrapper(cgosys_menu)
kill_proc.kill()
