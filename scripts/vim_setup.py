#!/usr/bin/env python3
"""Configure vim settings in Ubuntu."""

import argparse
from typing import Any

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import copy_files
from library.utilities import min_python_version
from library.utilities import wrap_tight


def run_script(e: Environment) -> None:
    """Configure vim.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    labels = Labels("""
        System initialization
        Creating new directories
        Copying files""")

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # Step 2. Creating new directory

    labels.next()
    p = e.HOME/'.vim/colors'
    if e.DEBUG:
        print(p)
    else:
        p.mkdir(parents=True, exist_ok=True)
    print(e.PASS)

    # Step 3. Copying files

    labels.next()
    targets: list[tuple[Any, Any]] = []
    targets.append((e.VIM/'vimrc.txt', e.HOME/'.vimrc'))
    targets.append((e.VIM/'vimcolors/*', e.HOME/'.vim/colors'))
    copy_files(e, targets)
    print(e.PASS)

    # Done

    msg = """vim setup complete. You are now ready to use vi or vim and
    enjoy a pleasing visual experience."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script installs the necessary settings files and
    color schemes for a pleasant visual experience in vi. NOTE: If
    you\'ve already run the ubuntu setup script there's no need to run
    this script."""

    epi = "Latest update: 12/02/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
