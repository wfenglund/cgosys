import os
import subprocess
import curses

def detect_games(rom_path):
    file_list = os.listdir(rom_path)
    game_dict = {}
    game_dict['gba'] = [i for i in file_list if i.endswith('.gba')]
    return game_dict

device = 'PowerA'
# device = 'keyboard'

config_dict = {}
config_dict['PowerA'] = 'powera_vbam.cfg'
config_dict['keyboard'] = 'keyboard_vbam.cfg'

device_config = config_dict[device]

gba_roms_path = './gba_roms/'
roms = detect_games(gba_roms_path)

def cgosys_menu(stdscr):
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
            for i in range(len(choices)):
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']
                stdscr.addstr(choices[i] + '\n', attr)
            character = stdscr.getch()
            if character == curses.KEY_UP and option > 0:
                option -= 1
            elif character == curses.KEY_DOWN and option < len(choices) - 1:
                option += 1
        choice = choices[option]
        if choice == 'Quit':
            break
        else:
            message = f'Running {choice}...'
            print(message, end = '\r')
            devnull = subprocess.DEVNULL
            subprocess.run(['vbam', '-c', device_config, f'{gba_roms_path}{choice}'], stdout = devnull, stderr = devnull)
            print(' ' * len(message), end = '\r')

curses.wrapper(cgosys_menu)
