import os
import subprocess

def detect_games(rom_path):
    file_list = os.listdir(rom_path)
    game_dict = {}
    game_dict['gba'] = [i for i in file_list if i.endswith('.gba')]
    return game_dict

def print_games(game_dict):
    print('# Available games:\n')
    for i in roms.keys():
        print(f'{i}:')
        for j in roms[i]:
            print(f'[{roms[i].index(j)}] {j}')
        print()

device = 'PowerA'
# device = 'keyboard'

config_dict = {}
config_dict['PowerA'] = 'powera_vbam.cfg'
config_dict['keyboard'] = 'keyboard_vbam.cfg'

device_config = config_dict[device]

gba_roms_path = './gba_roms/'
roms = detect_games(gba_roms_path)

while True:
    print_games(roms)
    print('[q] Quit\n')
    choice = input('Select game to play (by number): ')
    if choice == 'q':
        break
    else:
        try:
            chosen_game = roms['gba'][int(choice)]
            print(f'Starting {chosen_game}...\n')
            subprocess.run(['vbam', '-c', device_config, f'{gba_roms_path}{chosen_game}'])
        except (IndexError, ValueError) as error:
            print(f'- Index does not exist, try another one.\n')
