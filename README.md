# <a id="top"></a> ubuntu

## *Note: this version of Ubuntu setup will support Python down to version 3.8.10. For Ubuntu setups with Python version 3.10 or greater, use [this repository](https://github.com/geozeke/ubuntu) instead*

<br>

<img src="https://drive.google.com/uc?export=view&id=1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc" width="120"/>

## VM Setup Guides (Start Here)

To install a new Ubuntu Virtual Machine using the tools in this repository,
follow the setup guide available here: [Ubuntu
Setup](https://sites.google.com/view/ubuntuvm)

## Included Tools

This repo manages a series of setup and maintenance scripts for Ubuntu VMs. I
started this repo for Cyber Operations classes at USNA, but it's broadened and
become useful for setting up Ubuntu VMs for any purpose.

* [setup.py](#setup)
* [usnapatch.py](#usnapatch)
* [pyenv_setup.py](#pyenv_setup)
* [pytools.py](#pytools)
* [tuneup.py](#tuneup)
* [cacheburn.py](#cacheburn)
* [docker_setup.py](#docker_setup)
* [vim_setup.py](#vim_setup)

### <a id="setup"></a> `setup.py`

This script sets up a new Ubuntu VM with the following software and settings:

* Create new directories to hold various settings/resource files.
* Copy new settings files for:
  * bash
  * zsh
  * profile
  * vi
* Set the correct file permissions for scripts.
* Initialize the terminal profile with a nicer color scheme.
* Install the following packages from the ppa:
  * gnome-text-editor
  * build-essential
  * libnss3-tools
  * pcscd
  * pcsc-tools
  * ccache
  * vim
  * tree
  * seahorse-nautilus
  * zsh
  * powerline
  * python3-pip
  * python3-venv
* Install the following software / tools from developer sites:
  * oh-my-zsh (GitHub)
  * Google Chrome (vendor site)
* Setup and configure a series of jupyter notebooks for introductory topics in
  Python. More information is [available
  here](https://github.com/geozeke/notebooks).
* Configure the gnome favorites in the application launcher.
* Setup a starter Python virtual environment located here: `~/.venv/env`.
* Tune system settings:
  * Disable auto screen lock.
  * Set idle timeout to 'never'.
  * Disable Ubuntu auto-updates.
  * Patch `/etc/fuse.conf` to un-comment `user_allow_other`. This permits
    starting programs from the command line when you're inside a directory in
    the share point.
  * Neatly arrange icons on the favorites launcher.
  * Clean up and delete temporary and unused files.

#### usage

Follow the [VM Setup Guides](#top).

[top](#top)

### <a id="usnapatch"></a> `usnapatch.py`

This script installs a patched openssl configuration file and runs the
necessary scripts to support networking on the USNA mission network.

#### usage

Follow the [VM Setup Guides](#top).

[top](#top)

### <a id="pyenv_setup"></a> `pyenv_setup.py`

This script sets up and installs the incredibly helpful utility
[pyenv](https://github.com/pyenv/pyenv). This utility allows you to install and
manage multiple versions of python, without breaking the system default
installation.

#### usage

`~/ubuntu38/scripts/pyenv_setup.py`

[top](#top)

### <a id="pytools"></a> `pytools.py`

This script installs the following Python tools. *Recommend activating a python
virtual environment before running this script*:

* jupyter
* jupyterlab
* pytest

#### usage

`~/ubuntu38/scripts/pytools.py`

[top](#top)

### <a id="tuneup"></a> `tuneup.py`

This script is used to keep the newly-created Ubuntu VM patched. It performs
the following updates:

* `sudo apt update && sudo apt upgrade`
* `sudo apt -y autoremove`
* `sudo apt -y autoclean`
* `sudo snap refresh`
* Pull updates to this repo to support patching if necessary.
* Synchronize jupyter notebooks to catch updates.

#### usage

An alias for this script is created when the VM is setup. To run the tuneup
script and get help, just enter: `tuneup -h`.

[top](#top)

### <a id="cacheburn"></a> `cacheburn.py`

This script is used to clean caches and temp files from the share point. The
following are deleted from `~/shares`:

Directories:

* `__pycache__`
* `.pytest_cache`
* `.ipynb_checkpoints`

Files:

* `Icon?`
* `desktop.ini`

#### usage

An alias for this script is created when the VM is setup. To run the cacheburn
script and get help, just enter: `cacheburn -h`.

[top](#top)

### <a id="docker_setup"></a> `docker_setup.py`

This standalone script will install [Docker
Engine](https://docs.docker.com/engine/), which is the underlying client-server
technology that builds and runs containers using Docker's components and
services. It also installs [Docker
Compose](https://docs.docker.com/get-started/08_using_compose/).

#### usage

`~/ubuntu38/scripts/docker_setup.py`

[top](#top)

### <a id="vim_setup"></a> `vim_setup.py`

This is a standalone script that allows you to install the necessary files and
settings to create a pleasant visual experience in vi. It's useful if you've
got a user account (with no sudo access) on a Linux server and you just want a
better look-and-feel for vi.

#### usage

`~/ubuntu38/scripts/vim_setup.py`

[top](#top)
