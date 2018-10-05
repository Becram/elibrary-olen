#!/bin/bash

die() {
    echo "$1" >&2
    exit 1
}


get_release() {
    # Does this commit have an associated release tag?
    git tag --points-at HEAD | tail -n1 2>/dev/null |
    sed -e 's/^release-s//'
}

make_name() {
    release=$(get_release)

    if [ -z "$release" ]; then
        die "No release tag found; quitting"
    fi

}
