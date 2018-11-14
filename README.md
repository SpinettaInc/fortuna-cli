# Fortuna Manager CLI

A command line interface for the Fortuna Manager project written in Python 2.7 using the following packages

  - pyfiglet
  - PyInquirer

### Installation

MVP requires [Python](https://www.python.org/downloads/) 2.7.x+ to run.

Install the package and run the setup command

```sh
$ python setup.py develop
```

### Run

You should be able to now run using just the command below:

```sh
$ fortuna
```

Which produces the output similar to:

```sh
running develop
running egg_info
creating fortuna.egg-info
writing requirements to fortuna.egg-info/requires.txt
writing fortuna.egg-info/PKG-INFO
writing top-level names to fortuna.egg-info/top_level.txt
writing dependency_links to fortuna.egg-info/dependency_links.txt
writing entry points to fortuna.egg-info/entry_points.txt
writing manifest file 'fortuna.egg-info/SOURCES.txt'
reading manifest file 'fortuna.egg-info/SOURCES.txt'
writing manifest file 'fortuna.egg-info/SOURCES.txt'
running build_ext
Creating /usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/fortuna.egg-link (link to .)
fortuna 0.0.0 is already the active version in easy-install.pth
Installing fortuna script to /usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/bin
...
Using /Library/Python/2.7/site-packages
Finished processing dependencies for fortuna==0.0.0
```

If you receive a command not found error, most likely you need to export the bin directory to your bash_profile

```sh
$ nano ~/.bash_profile
export PATH="/usr/local/Cellar/python/2.7.11/Frameworks/Python.framework/Versions/2.7/bin/:$PA
```

