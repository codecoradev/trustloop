#!/usr/bin/env bash
set -eu
cp -R "$(dirname "$0")/files/." .
if [ -f setup-repo.sh ]; then bash setup-repo.sh && rm -f setup-repo.sh; fi
