#!/usr/bin/env bash

set -xe

poetry install

# poetry run main \
#        --walker "checker" \
#        --walk_root /lustre/scratch123/hgi/projects/crohns/mercury/hgi-vault-dev/python/no_git

poetry run main \
       --walker "checker" \
       --walk_root /lustre/scratch114/projects/crohns
