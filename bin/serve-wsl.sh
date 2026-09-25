#!/usr/bin/env bash
# Local preview on Windows via WSL (no Docker, no sudo).
#   From Windows:  wsl bash bin/serve-wsl.sh        -> http://localhost:4000/
# One-time setup (already done on this machine):
#   ~/miniconda3/bin/conda create -n jekyll -c conda-forge --override-channels ruby=3.4 imagemagick make compilers
#   gem install bundler -v 4.0.6 && bundle install
set -euo pipefail
export PATH="$HOME/miniconda3/envs/jekyll/bin:$PATH"
export BUNDLE_PATH="$HOME/.gems/homepage"
cd "$(dirname "$0")/.."
bundle install --quiet
# /mnt/d has no inotify, so poll for changes; write the site to WSL-local disk for speed.
exec bundle exec jekyll serve --host 0.0.0.0 --port 4000 --force_polling --livereload \
  --destination /tmp/homepage-site "$@"
