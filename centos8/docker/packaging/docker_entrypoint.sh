#!/bin/bash
set -e

gpg --import /keys/mormjbkey_sec.gpg
#git clone https://github.com/mormj/pkg-scripts

## If not cloning but using the local copy
cd /pkg-scripts/centos8/

exec "$@"