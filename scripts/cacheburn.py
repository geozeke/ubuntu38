#!/usr/bin/env python3
"""Clean up cache files and directories."""

import argparse

from library.classes import Environment
from library.classes import Labels
from library.utilities import min_python_version
from library.utilities import run_one_command


def burn_it_up(e: Environment) -> None:
    """Perform cached file cleaning operation.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    labels = Labels("""
        Deleting __pycache__ directories
        Deleting .pytest_cache directories
        Deleting .ipynb_checkpoints directories
        Zapping pesky Icon files
        Crunching annoying desktop.ini files""")

    # Start with cache directories:

    # NOTE: If this command were being run on the command line, you'd need to
    # escape the semicolon (\;)
    home = e.HOME/'shares'
    base = f'find {home} -name DIR -type d -exec rm -rvf {{}} ; -prune'
    commands: list[str] = []
    commands.append(base.replace('DIR', '__pycache__'))
    commands.append(base.replace('DIR', '.pytest_cache'))
    commands.append(base.replace('DIR', '.ipynb_checkpoints'))
    for cmd in commands:
        labels.next()
        print(run_one_command(e, cmd))

    # Tee up files for deletion. You can sneak some other options in for the
    # find command if necessary.

    base = f'find {home} -name FILE -type f -delete'
    commands = []
    commands.append(base.replace('FILE', 'Icon? -size 0'))
    commands.append(base.replace('FILE', 'desktop.ini'))
    for cmd in commands:
        labels.next()
        print(run_one_command(e, cmd))

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will scan the ~/shares directory to wipe caches
    and delete other temporary files."""

    epi = "Latest update: 12/02/22"

    parser = argparse.ArgumentParser(description=msg,
                                     epilog=epi,
                                     prog='cacheburn')

    parser.parse_args()
    print()
    burn_it_up(e)
    print()

    return


if __name__ == '__main__':
    main()
