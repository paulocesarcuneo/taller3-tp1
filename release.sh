#!/usr/bin/env bash
set -euo pipefail

echo $(( $(cat public/version) + 1 )) > public/version

zip "site-$(cat public/version).zip" -r public requirements.txt *.py

git add .
git commit -m "Release $(cat public/version)"
git tag -a "$(cat public/version)" -m "Release $(cat public/version)"
