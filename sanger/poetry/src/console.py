import logging
import os
from pathlib import Path
import stat

import click
from logdecorator import log_on_end, log_on_error, log_on_start

# from logdecorator import log_exception, log_on_end, log_on_error, log_on_start

from src.permissions import check_permissions, fix_permissions
from . import __version__


@log_on_start(
    logging.DEBUG, "start walk(walk_root_:{walk_root_:s}, walker_:{walker_.__name__:s})"
)
@log_on_error(logging.DEBUG, "error: {e!r},", on_exceptions=IOError, reraise=True)
@log_on_end(
    logging.DEBUG, "end walk(walk_root_:{walk_root_:s}, walker_:{walker_.__name__:s})"
)
def walk(walk_root_, walker_):
    ROOT = Path(walk_root_)

    walker_.Walker(ROOT)


@click.command()
@click.option(
    "--walker",
    default="checker",
    type=click.Choice(["checker", "fixer"], case_sensitive=False),
    help="walker function",
)
@click.option(
    "--walk_root", required=False, type=click.Path(exists=True), help="Root dir to Walk"
)
@click.version_option(version=__version__)
@log_on_start(logging.DEBUG, "start main()")
@log_on_end(logging.DEBUG, "end main()")
def main(walk_root, walker):
    logging.basicConfig(level=logging.DEBUG)
    click.secho("package src at version " + __version__, fg="green")

    # Mask for permissions for others (not in group).
    os.umask(stat.S_IRWXO)

    if walker == "checker":
        walk(walk_root, check_permissions)
    elif walker == "fixer":
        walk(walk_root, fix_permissions)
