#!/usr/bin/env python3
"""Install Python development tools."""

import argparse

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_one_command
from library.utilities import wrap_tight


def run_script(e: Environment) -> None:
    """Install Python development tools.

    Parameters
    ----------
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    labels = Labels("""
        System initialization
        Installing jupyter
        Installing jupyter lab
        Installing pytest""")

    # Step 1. System initialization. Right now it's just a placeholder for
    # future capability.

    labels.next()
    print(e.PASS)

    # Step 2, 3, 4 Install jupyter, jupyterlab & pytest

    base = 'pip3 install --upgrade TARGET'
    commands: list[str] = []
    commands.append(base.replace('TARGET', 'jupyter'))
    commands.append(base.replace('TARGET', 'jupyterlab'))
    commands.append(base.replace('TARGET', 'pytest'))
    for cmd in commands:
        labels.next()
        print(run_one_command(e, cmd))

    # Done

    msg = """Python tools installation complete. Install additional
    tools if desired. No reboot is necessary."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script will install several Python tools.
    Specifically: jupyter, jupyterlab, and pytest. It\'s recommend that
    you create and activate a Python virtual environment before running
    this script, or skip this script and install the tools in a Python
    virtual environment manually."""

    epi = "Latest update: 12/02/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)
    parser.parse_args()
    run_script(e)

    return


if __name__ == '__main__':
    main()
