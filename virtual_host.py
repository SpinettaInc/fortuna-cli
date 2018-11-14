import json
import sys
import os
import subprocess


def config_file(client_name=None, app_name=None, custom_server_name=None):
  """
  Generates a config file for apache based on clients app name

  """

  # Apache configs
  conf = app_name.split('_',1)[0] + '.conf'
  conf_copy = app_name.split('_',1)[0] + '.conf_copy'

  # Use these to replace the tags in the template config files
  client_tag = '<client_dns>'
  client_name_tag = '<client>'
  server_alias = '<server_alias>'
  custom_server_alias = '<custom_server_alias>'
  dns = client_name + '.fortuna.asia'
  result = ''

  if 'django' in app_name:
    os.chdir('../')
  with open(conf, 'r+') as conf_file:
    for line in conf_file:
      if client_tag in line:
        replaced_line = line.replace(client_tag, dns)
        result += replaced_line
      elif client_name_tag in line:
        replaced_line = line.replace(client_name_tag, client_name)
        result += replaced_line
      elif server_alias in line:
        replaced_line = line.replace(server_alias, app_name + '.' + client_name + '.mvp.fortuna.asia')
        result += replaced_line
      elif custom_server_alias in line:
        replaced_line = line.replace(custom_server_alias, 'www.' + custom_server_name)
        result += replaced_line
      else:
        result += line

  with open(conf_copy, 'w') as sub_apache_conf:
    sub_apache_conf.write(result)
  subprocess.call(['rm', conf])
  subprocess.call(['mv', conf_copy, dns + '.conf'])
  create_app_dirs(app_name.split('_',1)[0], dns + '.conf')


def create_app_dirs(app_name=None, conf_file=None):
  """ Create app dirs under the apache settings then reload the service """

  apache_conf_dir = '/etc/apache2/sites-available/'
  subprocess.call(['sudo', 'cp', '-p', conf_file, apache_conf_dir + conf_file])
  subprocess.call(['ls', '-l', '/etc/apache2/sites-available/'])