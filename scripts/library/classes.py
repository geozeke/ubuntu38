#!/usr/bin/env python3
"""Support classes for ubuntu setup scripts."""

import sys
from pathlib import Path


class Environment:
    """Class for holding environment variables.

    This class sets up the environment for the ubuntu scripts. All the
    paths, debugging flags, and pass/fail glyphs are created and
    initialized here.
    """

    def __init__(self):

        # Minimum required python version for Ubuntu VM scripts.

        self.MAJOR = 3
        self.MINOR = 10

        # PASS and FAIL markers; flag for enabling debug mode; and an
        # environment variable to hold the result from running commands using
        # sub-process. These results may be needed in future use cases.

        GREEN = '\033[0;32;49m'
        RED = '\033[0;31;49m'
        COLOR_END = '\x1b[0m'

        self.PASS = f'{GREEN}\u2714{COLOR_END}'
        self.FAIL = f'{RED}\u2718{COLOR_END}'
        self.DEBUG = False
        self.RESULT = None

        # Paths in the repo for installation files.

        self.HOME = Path.home()
        # Ubuntu is resolved in relation to this file (classes.py) to
        # facilitate debugging. The repo should still be cloned in ~ per the
        # setup instructions..
        self.UBUNTU = Path(__file__).resolve().parents[2]
        self.OHMYZSH = self.HOME/'.oh-my-zsh'
        self.SCRIPTS = self.UBUNTU/'scripts'
        self.SHELL = self.UBUNTU/'shell'
        self.SYSTEM = self.UBUNTU/'system'
        self.VIM = self.UBUNTU/'vim'


class ExhaustedListError(Exception):
    """Exception when attempting to pop elements from an empty list.

    Parameters
    ----------
    Exception : Python Exception type
        ExhaustedListError is a sub-class of Python's Exception class.
    """

    def __init__(self):
        self.message = "Cannot remove label, list of labels is empty."
        super().__init__(self.message)


class Labels:
    """Class to manage status labels in ubuntu scripts."""

    def __init__(self, s: str) -> None:
        """Create a new Labels object.

        Parameters
        ----------
        s : str
            This is a docstring that has one label per line, the
            initializer will repackage it into a list, along with an int
            variable (pad) that represents the length of the longest
            label. This is used for justifying the output when printing.
        """
        # The (t := token.strip()) part of the list comprehension below is
        # python's assignment expression and takes care of any blank lines or
        # leading/trailing whitespace in the docstring. It assigns
        # token.strip() to t then evaluates t. If t is an empty string, it
        # evaluates to False otherwise it's True.
        self.labels = [t for token in s.split('\n') if (t := token.strip())]
        self.pad = len(max(self.labels, key=len)) + 3
        return

    def next(self) -> None:
        """Print the next label (the one at position 0).

        Raises
        ------
        ExhaustedListError
            If attempting to pop from an empty list.
        """
        if len(self.labels) == 0:
            raise ExhaustedListError()
        print(f'{self.labels.pop(0):.<{self.pad}}', end='', flush=True)
        return

    def pop_first(self) -> str:
        """Pop and return the first label (position 0).

        Returns
        -------
        str
            A label.

        Raises
        ------
        ExhaustedListError
            If attempting to pop from an empty list.
        """
        if len(self.labels) == 0:
            raise ExhaustedListError()
        return self.labels.pop(0)

    def pop_last(self) -> str:
        """Pop and return the last label (position -1).

        Returns
        -------
        str
            A label.

        Raises
        ------
        ExhaustedListError
            If attempting to pop from an empty list.
        """
        if len(self.labels) == 0:
            raise ExhaustedListError()
        return self.labels.pop(-1)

    def pop_item(self, index: int) -> str:
        """Pop a label from a given index.

        Parameters
        ----------
        index : int
            The index to pop from.

        Returns
        -------
        str
            The popped label.

        Raises
        ------
        ExhaustedListError
            If attempting to pop from an empty list.
        """
        if len(self.labels) == 0:
            raise ExhaustedListError()
        try:
            label = self.labels.pop(index)
            return label
        except IndexError as e:
            print(f'{e}. Attempting to pop index {index}.')
            print('Terminating program.')
            sys.exit(1)

    def dump(self, num_labels: int) -> None:
        """Dump the given number of labels.

        Some operations require skipping (dumping) a certain number of
        labels that are not needed. This method will run down the label
        list, starting at [0], dumping the specified number of labels.

        Parameters
        ----------
        num_labels : int
            The number of labels to dump.
        """
        if ((type(num_labels) != int) or
                (num_labels <= 0) or (len(self.labels) < num_labels)):
            return
        else:
            self.labels = self.labels[num_labels:]
        return


if __name__ == '__main__':
    pass
