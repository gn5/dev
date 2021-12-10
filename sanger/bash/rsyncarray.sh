#!/usr/bin/env bash

# group of files and dirs must be crohns,
# and prevent others from having rights on files or dirs:
#
# newgrp ibdx10
# umask 007 # u=rwx,g=rwx,o=
#
# bsub: b rsyncarray.sh 2 10 long 

set -ex

out_dir="/lustre/scratch118/humgen/hgi/projects/ibdx10/variant_calling/joint_calling/ibd_concat_nextflow_backups"

declare -a arr=(
                "/lustre/scratch118/humgen/hgi/projects/ibdx10/variant_calling/joint_calling/ibd_concat_nextflow"
                "/lustre/scratch118/humgen/hgi/projects/ibdx10/variant_calling/joint_calling/ibd_concat_nextflow2"
                "/lustre/scratch118/humgen/hgi/projects/ibdx10/variant_calling/joint_calling/ibd_concat_nextflow3"
                "/lustre/scratch118/humgen/hgi/projects/ibdx10/variant_calling/joint_calling/ibd_concat_nextflow3_big"
                )

rsync_ () {
    local source=$1
    local todir=$2
    local logfile=$3
    echo started `date '+%d/%m/%Y_%H:%M:%S'` $source $todir >> $logfile
    # ignore original permissions, and  match target project permissions/umask.
    rsync -avP -s --no-p --no-g --chmod=ugo=rwX $source $todir
    echo finished `date '+%d/%m/%Y_%H:%M:%S'` $source $todir >> $logfile
}

for i in "${arr[@]}"
do
    rsync_ \
	"$i" \
	"${out_dir}/" \
	"${out_dir}/backup.log"
done

echo rsync done
