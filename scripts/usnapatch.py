#!/usr/bin/env python3
"""Patch files and run scripts to support network connections at USNA.

Raises
------
RuntimeError
    If Python is not at the minimum required version.
"""

import argparse
import tempfile
from pathlib import Path

from library.classes import Environment
from library.classes import Labels
from library.utilities import clear
from library.utilities import min_python_version
from library.utilities import run_many_arguments
from library.utilities import run_one_command
from library.utilities import wrap_tight

CERTFILE = 'apt.cs.usna.edu/ssl/system-certs-5.6-pa.tgz'


def find_db_files(starting: Path) -> list[Path]:
    """Find certificate db files.

    In this case, a certificate db file is any file that starts with
    'cert*' and has a '.db' extension.

    Parameters
    ----------
    starting : Path
        The directory to start a recursive search for db files.

    Returns
    -------
    list[Path]
        A list of fully-expressed pathlib objects for all db instances
        found.
    """
    L: list[Path] = []
    for p in starting.rglob('*'):
        if p.name.startswith('cert') and p.suffix == '.db':
            L.append(p)
    return L


def run_script(args: argparse.Namespace, e: Environment) -> None:
    """Patch openssl configuration and run certificate scripts.

    Parameters
    ----------
    args : argparse.Namespace
        This will contain the argparse object, which allows us to
        extract the mode. The mode determines which operation to
        perform: system, browser.
    e : Environment
        All the environment variables saved as attributes in an
        Environment object.
    """
    clear()

    # ------------------------------------------

    # Setup status labels

    labels = Labels("""
        Pulling updated USNA enterprise certificates
        Patching openssl configuration
        Removing old certificates
        Creating fresh directories
        Copying new certificates
        Running update utilities
        Finding certificate databases in user\'s home
        Updating certificate databases
        Cleaning up""")

    # ------------------------------------------

    # Step 0: Capture sudo permissions

    print("\nPlease enter your password if prompted.\n")
    # Push a dummy sudo command just to force password entry before first
    # command. This will avoid having the password prompt come in the middle of
    # a label when providing status
    run_one_command(e, 'sudo ls')

    # ------------------------------------------

    # Step 1: System initialization. Get the updated certificates from the USNA
    # server.

    labels.next()
    certdir = Path(tempfile.NamedTemporaryFile().name)
    certlist: list[Path] = []
    certdir.mkdir(parents=True)
    commands: list[str] = []
    commands.append(f'curl -o {certdir}/certs.tgz {CERTFILE}')
    commands.append(f'tar -xpf {certdir}/certs.tgz -C {certdir}')
    for command in commands:
        result = run_one_command(e, command)
        if result == e.FAIL:
            break

    # Create a list of all the full pathnames for the certificates
    if result == e.PASS:
        for p in certdir.iterdir():
            if p.is_file and p.suffix == '.crt':
                certlist.append(p)

    print(result)

    # ------------------------------------------

    # Step 2: Take action based on selected options.

    match args.mode:

        case 'system':
            # Patch openssl configuration
            labels.next()
            target = '/usr/lib/ssl/openssl.cnf'
            cmd = f'sudo cp -f {e.SYSTEM}/openssl.cnf {target}'
            print(run_one_command(e, cmd))

            # Clean out any old certificates:
            labels.next()
            dir1 = '/usr/share/ca-certificates/dod'
            dir2 = '/usr/local/share/ca-certificates/dod'
            targets: list[str] = []
            targets.append(dir1)
            targets.append(dir2)
            cmd = 'sudo rm -rf TARGET'
            print(run_many_arguments(e, cmd, targets))

            # Create fresh directory
            labels.next()
            cmd = f'sudo mkdir -p {dir2}'
            print(run_one_command(e, cmd))

            # Copy certificates to new directory
            labels.next()
            for cert in certlist:
                cmd = f'sudo cp {cert} {dir2}'
                result = run_one_command(e, cmd)
                if result == e.FAIL:
                    break
            print(result)

            # Run the update utility
            labels.next()
            cmd = 'sudo update-ca-certificates -f'
            print(run_one_command(e, cmd))

            # Dump unused labels:
            labels.dump(2)

        case 'browser':
            # Dump unused labels
            labels.dump(5)

            # From the user's home directory, look for certificate database
            # files inside any hidden directory (starting with '.')
            labels.next()
            cert_databases: list[Path] = []
            for p in Path.home().iterdir():
                if p.is_dir and p.name.startswith('.'):
                    cert_databases += find_db_files(p)
            print(e.PASS)

            # Once any / all certificate databases are found, update them with
            # the certutil utility using the certificates taken from the USNA
            # server.
            labels.next()
            result = e.PASS
            for db in cert_databases:
                cmd_root = f'certutil -d sql:{db.parent} -A -t \"TC\"'
                for cert in certlist:
                    cmd = f'{cmd_root} -n {cert.stem} -i {cert}'
                    result = run_one_command(e, cmd)
                    if result == e.FAIL:
                        break
                if result == e.FAIL:
                    break
            print(result)

        case _:
            pass

    # ------------------------------------------

    # Step 3: Cleanup temporary directories

    labels.next()
    cmd = f'rm -rf {certdir}'
    print(run_one_command(e, cmd))

    # ------------------------------------------

    msg = """Patch script is complete. If all steps above are marked
    with green checkmarks, the certificate patching was successful. If
    any steps above show a red \"X\", there was an error during
    certificate modification."""
    print(f'\n{wrap_tight(msg)}\n')

    return


def main():  # noqa

    # Get a new Environment variable with all the necessary properties
    # initialized.
    e = Environment()
    if (result := min_python_version(e)):
        raise RuntimeError(result)

    msg = """This script installs a patched openssl configuration file
    and runs the necessary certificate patching utilities to support
    networking on the USNA mission network. You will be prompted for
    your password during installation."""

    epi = "Latest update: 12/02/22"

    parser = argparse.ArgumentParser(description=msg, epilog=epi)

    msg = """Include one of the following options indicating where
    to apply patches: system, browser"""
    parser.add_argument('mode',
                        choices=['system', 'browser'],
                        type=str,
                        help=msg)

    args = parser.parse_args()
    run_script(args, e)

    return


if __name__ == '__main__':
    main()
