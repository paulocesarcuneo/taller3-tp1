#!/usr/bin/env bash
set -euo pipefail

echo $(( $(cat public/version) + 1 )) > public/version

zip site.zip -r public visits.py main.py requirements.txt

git add .
git commit -m "Release $(cat public/version)"
git tag -a "$(cat public/version)" -m "Release $(cat public/version)"
