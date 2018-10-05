#!/bin/bash

die() {
    echo "$1" >&2
    exit 1
}

RELEASE_TAG=$(git describe --abbrev=0 --tags | sed -e 's/^release-//')

if [ -z "$RELEASE_TAG" ]; then
       die "No release tag found; quitting"
fi

grep -q 'stable' build.yml
if [ $? -eq 0 ]; then
    sed -i.bak "s/\bstable-[^ ]*/${RELEASE_TAG}/g" build.yml
else
    echo "Failed to build because there is no version in build.yml file"
    exit 1
fi
# docker-compose -f build.yml build
# echo "done building at $(date) "touch /tmp/deploy
