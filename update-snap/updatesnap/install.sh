#!/bin/sh

mkdir -p /usr/local/bin

./mix_modules.py updatesnap.py /usr/local/bin
./mix_modules.py updatesnapyaml.py /usr/local/bin
