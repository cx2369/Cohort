#!/bin/bash

WORKDIR="/home/cas/chenxu/cxfuzz3"
AFLPPDIR="$WORKDIR/aflpp"
BACKDIR="/home/cas/chenxu/cxfuzz3-backup"

# copy file to backup folder

cp $AFLPPDIR/src/*.{c,cc} $BACKDIR

cp $AFLPPDIR/instrumentation/*.{c,cc} $BACKDIR

cp $AFLPPDIR/include/* $BACKDIR

cp $WORKDIR/script/* $BACKDIR

cp $AFLPPDIR/GNUmakefile $BACKDIR

cp $AFLPPDIR/GNUmakefile.llvm $BACKDIR

cd /home/cas/chenxu/cxfuzz3-backup
rm aaacxfuzz3.bundle
git add -A
git commit -m "cxfuzz3"
git bundle create aaacxfuzz3.bundle --all


