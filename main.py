import secrets
import pathlib
import sys
from dearpygui.core import *
from dearpygui.simple import *
from pyautogui import size
import pyperclip

wl = getattr(sys, "_MEIPASS", pathlib.Path(__file__).resolve().parent) / pathlib.Path("data/wordlist.txt")
pwds = []


def generate_pwd():
    try:
        wordlist = open(file=wl).read().splitlines()
    except IOError:
        if does_item_exist('err_win'):
            delete_item('err_win')
        with window(name='err_win', label='Error', no_resize=True, autosize=True, no_move=True,
                    x_pos=0, y_pos=0):
            add_dummy()
            add_text(name='Cannot open wordlist.txt file.\nYou can try running app in\nADMIN mode.',
                     color=[250, 25, 25, 200])
        return
    # Get options
    num_of_pwds = get_value(name='##n_of_pwds')
    num_of_wrds = get_value(name='##n_of_wrds')
    joiner = get_value(name='##cjoiner')
    if joiner == 'space':
        joiner = ' '
    inc_letter = get_value(name='##check_letter')
    inc_num = get_value(name='##check_num')
    # Generate passwords
    pwds.clear()
    for _ in range(num_of_pwds):
        pwd = []
        for _ in range(num_of_wrds):
            pwd.append(secrets.choice(wordlist))
        if inc_letter:
            pwd[0] = pwd[0].capitalize()
        if inc_num:
            pwd.append(str(secrets.randbelow(10)))
        pwds.append(joiner.join(pwd))
    pwds_text = '\n'.join(pwds)
    # Show passwords
    if does_item_exist('##it_pwds'):
        delete_item('##it_pwds')
    add_input_text(name='##it_pwds', label='', parent='main_window', default_value=pwds_text, readonly=True,
                   multiline=True, width=int(50 + num_of_wrds * 42), height=int(20 + num_of_pwds * 12))


def copy():
    if does_item_exist('##it_pwds'):
        pyperclip.copy(pwds[0])
    else:
        generate_pwd()
        pyperclip.copy(pwds[0])


def start():
    with window(name='main_window', label='PyPassGen', no_resize=True):
        add_dummy()
        add_text(name='Number of passwords: ')
        add_input_int(name='##n_of_pwds', min_value=1, max_value=50, default_value=10)
        add_dummy()
        add_text(name='Number of words to join: ')
        add_input_int(name='##n_of_wrds', min_value=3, max_value=10, default_value=5)
        add_dummy()
        add_text(name='Join with: ')
        add_combo(name='##cjoiner', items=['-', '_', 'space', '+', '.', ';', '/', ','], default_value='-')
        add_dummy()
        add_separator()
        add_dummy()
        add_text(name='Include capital letter?')
        add_checkbox(name='##check_letter', default_value=True)
        add_dummy()
        add_text(name='Include number?')
        add_checkbox(name='##check_num', default_value=True)
        add_dummy()
        add_dummy()
        add_dummy()
        add_button(name='gen_btn', label='Generate', callback=generate_pwd)
        add_same_line()
        add_dummy(width=45)
        add_same_line()
        add_button(name='copy_btn', label='Copy First', callback=copy)

    # Center app on screen
    screen_width, screen_height = size()
    set_main_window_size(width=250, height=450)
    set_main_window_pos(x=int(screen_width / 4), y=int(screen_height / 4))
    # Start DearPyGUI
    set_main_window_title(title='PyPassGen')
    start_dearpygui(primary_window='main_window')


if __name__ == '__main__':
    start()



