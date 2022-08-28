import os
import random


def is_valid_name(label):
    list_labels = os.listdir('voices')
    for x in list_labels:
        if x == (label + '.mp3'):
            return False
    return True


def extract_key(message_text):
    key = ''

    for i in range(len(message_text)):
        if i > 6:
            key = key + message_text[i]
    return key


def is_key_correct(key):
    try:
        if int(key) >= 0:
            if int(key) <= len(os.listdir('voices')):
                return True
        return False
    except:
        if key == '':
            return True
        return False


def get_voice_dir(key):
    if key == '' or key == '0':
        index = random.randint(0, len(os.listdir('voices')))
        return 'voices/' + os.listdir('voices')[index]
    else:
        return 'voices/' + os.listdir('voices')[int(key) - 1]


def get_list():
    text = 'List: '
    for x in range(len(os.listdir('voices'))):
        text = text + '\n    ' + str(x+1) + ': ' + os.listdir('voices')[x]
    return text
