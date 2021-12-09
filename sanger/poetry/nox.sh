#!/usr/bin/env bash
set -xe

source /software/hgi/installs/anaconda3/envs/py310/venv/bin/activate

nox --reuse-existing-virtualenvs --stop-on-first-error
