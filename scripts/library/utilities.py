#!/usr/bin/env python3
"""Utilities for ubuntu scripts."""

import os
import pathlib
import shlex
import shutil
import subprocess as sp
import sys
import textwrap
from typing import Text
from typing import TextIO

from .classes import Environment


def clear() -> None:
    """Clear the screen.

    This is an os-agnostic version, which will work with both Windows
    and Linux.
    """
    os.system('clear' if os.name == 'posix' else 'cls')


def clean_str(bstr: bytes) -> Text:
    """Convert a bytestring.

    Performs the utf-8 conversion of a byte stream and strips any
    trailing white space or newline characters

    Parameters
    ----------
    bstr : bytes
        A byte string to be converted.

    Returns
    -------
    Text
        A utf-8 string.
    """
    return bstr.decode('utf-8').rstrip()


def wrap_tight(msg: str, columns=70) -> str:
    """Clean up a multi-line docstring.

    Take a multi-line docstring and wrap it cleanly as a paragraph to a
    specified column width.

    Parameters
    ----------
    msg : str
        The docstring to be wrapped.
    columns : int, optional
        Column width for wrapping, by default 70.

    Returns
    -------
    str
        A wrapped paragraph.
    """
    clean = ' '.join([t for token in msg.split('\n') if (t := token.strip())])
    return textwrap.fill(clean, width=columns)


def run_one_command(e: Environment,
                    cmd: str,
                    capture: bool = True,
                    std_in: TextIO | None = None,
                    std_out: TextIO | None = None) -> Text:
    """Run a single command in the shell.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    cmd : str
        A shell command (with potentially options) saved as a Python
        string.
    capture : bool, optional
        Determine if stdout should be suppressed (True) or displayed
        (False), by default True.
    std_in : TextIO | None
        If stdin needs to be redirected on the command line you can
        pass an open file descriptor here for that purpose, by default
        None.
    std_out : TextIO | None
        If stdin needs to be redirected on the command line you can
        pass an open file descriptor here for that purpose, by default
        None.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    if e.DEBUG:
        print(f'\nRunning: {shlex.split(cmd)}')
        return e.PASS
    else:
        e.RESULT = sp.run(shlex.split(cmd),
                          capture_output=capture,
                          stdin=std_in,
                          stdout=std_out)
        if e.RESULT.returncode != 0:
            return e.FAIL
    return e.PASS


def run_many_arguments(e: Environment,
                       cmd: str,
                       targets: list[str],
                       marker: str = 'TARGET') -> Text:
    """Run the same command with multiple arguments.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    cmd : str
        A shell command (with potentially options) saved as a Python
        string.
    targets : list[str]
        A Python list of strings representing the different arguments
        to be used on multiple runs of the command.
    marker : str, optional
        A string representing the replacement marker in the command
        string. Every time the command is run, a new target will be put
        in place of the marker. By default 'TARGET'.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    for target in targets:
        result = run_one_command(e, cmd.replace(marker, target))
        if result == e.FAIL:
            return result
    return result


def copy_files(e: Environment,
               targets: list[tuple[pathlib.Path, pathlib.Path]]) -> None:
    """Copy files from source to destination.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    targets : list[tuple[pathlib.Path, pathlib.Path]]
        A list of tuples. Files will be copied from source [0] to
        destination [1].
    """
    for target in targets:
        copy_from, copy_to = target[0], target[1]
        if e.DEBUG:
            print(f'\nCopying: {str(copy_from)}\nTo: {str(copy_to)}')
        else:
            if '*' in copy_from.name:
                for file in copy_from.parent.resolve().glob(copy_from.name):
                    shutil.copy(file, copy_to)
            else:
                shutil.copy(copy_from, copy_to)
    return


def sync_notebooks(e: Environment) -> Text:
    """Synchronize jupyter notebooks.

    Sync the hidden repository with the local notebooks directory. Use
    the --delete option so the destination directory always exactly
    mirrors the source directory. Also use the --delete-excluded option
    in case a stray file from the source, which should be excluded,
    makes its way to the destination. Per the man page, leaving a
    trailing slash ('/') on the source directory allows you to sync the
    contents of the source directory to a destination directory with a
    different name.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.

    Returns
    -------
    Text
        Returns a unicode string representing either a green checkmark
        (PASS) or a red X (FAIL).
    """
    src = f'{e.HOME}/.notebooksrepo/'
    dest = f'{e.HOME}/notebooks'
    exclude = f'{e.SYSTEM}/rsync_exclude.txt'
    options = f'-rc --exclude-from={exclude} --delete --delete-excluded'
    cmd = f'rsync {src} {dest} {options}'
    return run_one_command(e, cmd)


def min_python_version(e: Environment) -> Text | None:
    """Determine if Python is at required min version.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.

    Returns
    -------
    str | None
        If Python is at the minimum version return None. If not,
        return a string error message.
    """
    msg = f'Minimum required Python version is {e.MAJOR}.{e.MINOR}'
    if ((sys.version_info.major < e.MAJOR) or
       (sys.version_info.minor < e.MINOR)):
        return msg
    return None


if __name__ == '__main__':
    pass
