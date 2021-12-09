#!/usr/bin/env bash

# group of files and dirs must be crohns,
# and prevent others from having rights on files or dirs:
#
# newgrp crohns
# umask 007 # u=rwx,g=rwx,o=
#
# bsub: b rsyncone.sh 2 10 long 

set -ex

s114="/lustre/scratch114/projects/crohns"
s123="/lustre/scratch123/hgi/mdt1/projects/crohns"

# done
torsync="/lustre/scratch114/projects/crohns/uk10k-exome" # 1.8 Gb
torsync="/lustre/scratch114/projects/crohns/rare_variants" # 3 tb
torsync="/lustre/scratch114/projects/crohns/somatic_ibd_p1" # 4 tb
torsync="/lustre/scratch114/projects/crohns/merge" # 11 tb
# end done

torsync="/lustre/scratch114/projects/crohns/ichip_vs_nonichip" # 113G

echo started `date '+%d/%m/%Y_%H:%M:%S'` ${torsync} ${s123}/mercury/backup114/ >> ${s123}/mercury/backup114/backup.log
# ignore original permissions, and  match target project permissions/umask.
rsync -avP -s --no-p --no-g --chmod=ugo=rwX ${torsync} ${s123}/mercury/backup114/
echo finished `date '+%d/%m/%Y_%H:%M:%S'` ${torsync} ${s123}/mercury/backup114/ >> ${s123}/mercury/backup114/backup.log

echo rsync done
