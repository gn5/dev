#!/usr/bin/env bash

# group of files and dirs must be crohns,
# and prevent others from having rights on files or dirs:
#
# newgrp crohns
# umask 007 # u=rwx,g=rwx,o=
#
# bsub: b rsyncarray.sh 2 10 long 

set -ex

s114="/lustre/scratch114/projects/crohns"
s123="/lustre/scratch123/hgi/mdt1/projects/crohns"

declare -a arr=(
		"/lustre/scratch114/projects/crohns/.TemporaryItems"
		"/lustre/scratch114/projects/crohns/SC_check"
		"/lustre/scratch114/projects/crohns/crohns-bridgebuilder"
		"/lustre/scratch114/projects/crohns/S04380110_Regions.bed"
		"/lustre/scratch114/projects/crohns/GWAS_imputation"
		"/lustre/scratch114/projects/crohns/submit.sh"
		"/lustre/scratch114/projects/crohns/uk10kdata_logs"
		"/lustre/scratch114/projects/crohns/uk10k-bridgebuilder"
		"/lustre/scratch114/projects/crohns/SCsamples.txt"
		"/lustre/scratch114/projects/crohns/event_counts_1.txt"
		"/lustre/scratch114/projects/crohns/RGfix"
		"/lustre/scratch114/projects/crohns/vvi"
		"/lustre/scratch114/projects/crohns/CNinfo.txt"
		"/lustre/scratch114/projects/crohns/fileloc.txt"
		"/lustre/scratch114/projects/crohns/psoriasis"
		"/lustre/scratch114/projects/crohns/._.TemporaryItems"
		"/lustre/scratch114/projects/crohns/master.list"
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
	"${s123}/mercury/backup114/" \
	"${s123}/mercury/backup114/backup.log"
done

echo rsync done
