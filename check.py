import os
import json
import app
from subprocess import call

def load_app_json(app_dir=None, app_name=None):
  """
  Check what apps need to be created

  """

  current_dir = os.path.dirname(os.path.realpath(__file__))
  template_dir = 'template_apps'
  files = os.listdir(current_dir + '/' + template_dir + '/' + app_name)

  for file in files:
    if file == app_name + '.json':
      path = current_dir + '/' + template_dir + '/' + app_name + '/' + file
      
      # Copy the template json file with the clients name, then build the app
      path_copy = current_dir + '/' + template_dir + '/' + app_name + '/copy_' + file
      call(['cp', '-p', path, path_copy])

      # Open the file and truncate new changes
      with open(path_copy, 'r+') as json_file:
        file = json.load(json_file)
        if 'command' in file.keys() and file['command']:
          file['command'] = file['command'].replace('<client_name>', app_dir + '_' + app_name)
        json_file.seek(0)
        json.dump(file, json_file, indent=2)
        json_file.truncate()

        context = {
          'json_copy': path_copy,
          'template_dir': current_dir + '/' + template_dir + '/',
        }
        return context