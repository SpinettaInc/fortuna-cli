import argparse
import os
import virtual_host
import app
import json
import check, virtual_host
from subprocess import call

def create_client_dir(client_dir=None):
  """Create client directories"""

  if not os.path.exists(client_dir):
      os.makedirs(client_dir)


def create_client_sub_dir(client_dir=None):
  """Create client sub directories"""

  os.chdir(client_dir)
  client_sub_dirs = ['config', 'apps', 'backups']
  for sub_dir in client_sub_dirs:
    if not os.path.exists(sub_dir):
      os.makedirs(sub_dir)


def copy_app_settings_dir(client_dir=None, app_name=None, json_dict=None):
  """ Copy the entire settings dir + files to the app """

  if 'template_dir' in json_dict.keys():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = json_dict['template_dir'] + app_name
    client_app_path = current_dir + '/config/'
    call(['cp', '-a', template_path, client_app_path])

    count = 0
    app_dirs = os.listdir(client_app_path)
    for app in app_dirs:
      if app_name in app_dirs:
        count += 1
  
    old_app_name = client_app_path + app_name
    new_app_name = client_app_path + app_name + '_' + str(count)
    call(['mv', old_app_name, new_app_name])
    app_name = app_name + '_' + str(count)

    # Remove the copied template json file since we no longer need it
    if os.path.exists(json_dict['json_copy']):
      os.remove(json_dict['json_copy'])

    # Remove the template and replace with the copy for this app
    copied_json = client_app_path + app_name + '/copy_' + app_name.split('_',1)[0] + '.json'
    template_json = client_app_path + app_name + '/' + app_name.split('_',1)[0] + '.json'

    # Rename the app yml file
    template_yml = client_app_path + app_name + '/' + app_name.split('_',1)[0] + '.yml'
    app_yml = client_app_path + app_name + '/docker-compose.yml'

    if os.path.exists(template_json):
      os.remove(template_json)
      os.rename(copied_json, template_json)
      os.rename(template_yml, app_yml)
    return app_name


def create_app_txt_file(app_details=None):
  """ Save app details into some text file for Django to read """

  # TODO: Change this to servers /usr/shared directory or something
  os.chdir(os.path.expanduser('~/Documents/jobstuff/spinetta/sprint/mvp_platform/backend/static/'))
  file = open('app_details.json','a')
  file.write(json.dumps(app_details, indent=4) + ',')
  call(['pwd'])


if __name__ =='__main__':
  """ Root of the program """

  current_dir = os.path.dirname(os.path.realpath(__file__))
  parser = argparse.ArgumentParser(description='''Run this script with the following format: python root.py --client=name --app=appname --vhost=vhostname''')
  parser.add_argument('--client', type=str, help='e.g. client_ikkai_benjamin')
  parser.add_argument('--app', type=str, help='e.g. drupal')
  parser.add_argument('--customservername', type=str, help='e.g. ben-inc.com')
  parser.add_argument('--webserver', type=str, default='httpd', help='e.g. httpd')
  parser.add_argument('--version', type=str, default='latest', help='e.g. 1.2')
  args = parser.parse_args()
  
  # Main args to build an app
  client_name = args.client
  app_name = args.app
  custom_server_name = args.customservername
  webserver = args.webserver
  version = args.version
  
  # Prepare json file with commands
  json_dict = check.load_app_json(client_name, app_name)

  # Create folders & app configs
  create_client_dir(client_name)
  create_client_sub_dir(client_name)
  app_name = copy_app_settings_dir(client_name, app_name, json_dict)

  url = app.create(client_name, app_name)

  # create a custom domain with vhost on our webserver
  virtual_host.config_file(client_name, app_name, custom_server_name)

  # Save app details & URL in a dict, into a temporary file for Django
  create_app_txt_file({'url': url, 'custom_url': custom_server_name, 'client': client_name, 'app': app_name})



