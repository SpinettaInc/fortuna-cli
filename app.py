import os
import json
import docker
import subprocess
from random import randint

def rename_app_dir(client_name=None, app_name=None):
  """ Rename the app directory with the container id """

  current_dir = os.path.dirname(os.path.realpath(__file__))
  current_dir += '/' + client_name + '/config/'

  os.chdir(current_dir)
  client = docker.from_env()
  containers = client.containers.list(all=True)
  container_id = containers[0].id

  old_app_name = current_dir + '/' + app_name
  new_app_name = current_dir + (container_id[:20])
  subprocess.call(['mv', old_app_name, new_app_name])


def randomize_port_no(path=None):
  """ Randomize the port number in docker-compose to avoid conflicts """

  os.chdir(path)
  randomized_port_no = ''
  result = ''

  # Default port settings
  web = '0000'
  db = '1111'

  # Override port settings
  web_port = '80' + str(randint(10, 99))
  db_port = '30' + str(randint(100, 999))

  # Need to update the docker-compose file. 
  # But we can't update it directly so its better to copy and then replace it
  with open('docker-compose.yml', 'r+') as yml_file:
    for line in yml_file:
      if web in line:
        randomized_port_no = web_port
        replace_line = line.replace(web, randomized_port_no)
        result += replace_line
      if db in line:
        replace_line = line.replace(db, db_port)
        result += replace_line
      else:
        result += line

  with open('docker-compose.yml_copy', 'w') as docker_compose_yml:
    docker_compose_yml.write(result)
  
  subprocess.call(['rm', 'docker-compose.yml'])
  subprocess.call(['mv', 'docker-compose.yml_copy', 'docker-compose.yml'])
  return randomized_port_no


def other_app_settings(client_name=None, app_name=None):
  """ Initialize Drupal specific settings """

  current_dir = os.path.dirname(os.path.realpath(__file__))
  current_dir += '/' + client_name + '/config/' + app_name + '/'
  port_no = randomize_port_no(current_dir)
  return port_no


def django_settings(client_name=None, app_name=None):
  """ Initialize Django specific settings """

  current_dir = os.path.dirname(os.path.realpath(__file__))
  current_dir += '/' + client_name + '/config/' + app_name + '/'
  port_no = randomize_port_no(current_dir)
  dns = client_name + '.mvp.fortuna.asia'

  # # Override and truncate local settings
  current_dir += client_name + '_' + app_name.split('_',1)[0] + '/'
  os.chdir(current_dir)
  if os.path.exists('settings.py'):
    with open('settings.py', 'a') as settings_py:
      allowed_hosts = 'ALLOWED_HOSTS = [\'0.0.0.0\', \''+ dns + '\']'
      settings_py.write(allowed_hosts)
  return port_no


def create(client_name=None, app_name=None):
  """ Create app using Docker compose """

  port_no = '8080'
  current_dir = os.path.dirname(os.path.realpath(__file__))
  client_app_path = current_dir + '/' + client_name + '/config/' + app_name

  # Change dir to app path and create app project using Docker
  os.chdir(client_app_path)
  file_name = client_app_path + '/' + app_name.split('_',1)[0] + '.json'
  with open(file_name, 'r') as app_json:
    file = json.load(app_json)
    # If there is preconfigured command settings, run them
    if file['command']: subprocess.call(file['command'].split())
    # Django specific setting
    if 'django' in app_name: port_no = django_settings(client_name, app_name)
    if 'drupal' in app_name: port_no = other_app_settings(client_name, app_name)
    if 'rails' in app_name: port_no = other_app_settings(client_name, app_name)
    
    # Run the containers if not already
    if 'no_of_commands' in file.keys():
      for no_of_commands, command in enumerate(file['run_command']):
        subprocess.call(command.split())
    else:
      if 'run_command' in file.keys():
        subprocess.call(file['run_command'].split())

  url = 'http://' + client_name + '.mvp.fortuna.asia:' + port_no
  return url

