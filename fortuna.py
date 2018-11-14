""" Fortuna Manager CLI
Usage:
    fortuna.py
    fortuna.py <command> <app>
    
    fortuna.py -h|--help
    fortuna.py -v|--version

    Where <command> = the command arguement. e.g. install, uninstall etc
    where <app> = App you want to install. e.g. django, drupal etc
Options:
    -h --help  Show this screen.
    -v --version  Show version.
"""

from __future__ import print_function, unicode_literals
from docopt import docopt
from pyfiglet import Figlet
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
import os
import json
import subprocess

# TODO: Change this to servers /usr/shared directory or something
dir_path = '~/Documents/jobstuff/spinetta/sprint/'

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#e455f4 bold',
    Token.Instruction: '',
    Token.Answer: '#ffd800 bold',
    Token.Question: '#9aed02',
})

class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def install(app=None):
    """ Run the CLI command to install app """
    f = Figlet(font='slant')
    print(f.renderText('Fortuna Manager CLI'))
    print('A CLI version of the Fortuna Manager portal')

    questions = [
        {
            'type': 'input',
            'name': 'client',
            'message': 'Tell me your name',
            'filter': lambda val: val.lower()
        },
        {
            'type': 'confirm',
            'name': 'custom_url_check',
            'message': 'Would you like a custom URL?',
            'default': False
        },
        {
            'type': 'input',
            'name': 'custom_url',
            'message': 'Please enter your custom URL',
            'filter': lambda val: val.lower(),
            'when': lambda answers: answers['custom_url_check'] != False
        },
    ]

    answers = prompt(questions, style=style)
    result = {k: '"' + v + '"' for k,v in answers.iteritems() if not isinstance(v, bool)}
    os.system('python root.py --client=' + result['client'] + ' --app=' + app + ' --customservername=' + result['custom_url'])


def uninstall():
    """ Run the CLI command to uninstall app """

    f = Figlet(font='slant')
    print(f.renderText('Fortuna Manager CLI'))
    print('A CLI version of the Fortuna Manager portal')
    os.chdir(os.path.expanduser(dir_path + 'mvp_platform/backend/static/'))
    file_str = ''
    with open('app_details.json','r') as file:
      for line in file:
        file_str += line

    valid_json_str =  "[{0}]".format(file_str[:-1])
    data = json.loads(valid_json_str)
    apps_list = [app['app'] for app in data]

    questions = [
        {
            'type': 'input',
            'name': 'client',
            'message': 'Tell me your name',
            'filter': lambda val: val.lower()
        },
        {
            'type': 'rawlist',
            'name': 'app',
            'message': 'Which app do you want to install?',
            'choices': apps_list
        },
        {
            'type': 'confirm',
            'name': 'app_confirm',
            'message': 'Are you sure you want to uninstall this app?',
            'default': False
        },
    ]

    result = prompt(questions, style=style)
    os.chdir(os.path.expanduser(dir_path + 'fortuna-manager/'))
    os.system('python uninstall.py --client=' + result['client'] + ' --app=' + result['app'])


def cmd_menu(cmd=None, app=None, doc=None):
    """ Decide what the user wants to do """

    if cmd == 'install':
        install(app)
    elif cmd == 'uninstall':
        uninstall()
    else:
        print(__doc__)


def main():
    arguments = docopt(__doc__, version='DEMO 1.0')
    if arguments['<command>']:
        cmd = arguments['<command>']
        app = arguments['<app>']
        cmd_menu(cmd, app)
    else:
        cmd_menu(cmd, app, __doc__)

if __name__ == '__main__':
    main()


