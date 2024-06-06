import pygame

### Initiate pygame and find controllers:
pygame.init()
controllers = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

def get_contr_press():
        if len(controllers) > 0:
            controllers[0].init()
            button_dict = {12:258, 11:259, 0:10, 7:7}
            events = pygame.event.get()
            if len(events) > 0:
                for press in events:
                    if 'button' in press.dict.keys():
                        button = press.dict['button']
#                         button = button_dict[button] if button in button_dict.keys() else ''
                        controllers[0].quit()
                        return press.dict
#                     if 'axis' in press.dict.keys():
#                         button = press.dict['axis']
#                         button = button_dict[button] if button in button_dict.keys() else ''
#                         controllers[0].quit()
#                         return button
                    else:
                        return press.dict
        return ''

# print(controllers)

while True:
    press = get_contr_press()
    if press != '':
        print(press)
