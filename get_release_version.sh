#!/bin/bash

die() {
    echo "$1" >&2
    exit 1
}

DATE=`date '+%Y-%m-%d %H:%M:%S'`
RELEASE_TAG=$(git describe --abbrev=0 --tags)

if [ -z "$RELEASE_TAG" ]; then
       die "No release tag found; quitting"
fi

grep -q 'stable' build.yml
if [ $? -eq 0 ]; then
	echo "Releasing version is ${RELEASE_TAG}"
    sed -i.bak "s/\{RELEASE_TAG\}/${RELEASE_TAG}/g" build.yml.template > build.yml
    sed -i.bak "s/\bstable-[^ ]*/${RELEASE_TAG}/g" production.yml.template > production.yml
else
    echo "Failed to build because there is no version in build.yml file"
    exit 1
fi

echo "${RELEASE_TAG} on $DATE" >> /library/media_root/release_version.txt
# docker-compose -f build.yml build
# echo "done building at $(date) "touch /tmp/deploy
