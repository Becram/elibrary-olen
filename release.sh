
#!/bin/bash

# Script to simplify the release flow.
# 1) Fetch the current release version
# 2) Increase the version (major, minor, patch)
# 3) Add a new git tag
# 4) Push the tag

#production branch
prodBranch=bikram-stack




# Parse command line options.
while getopts ":Mmpd" Option
do
  case $Option in
    M ) major=true;;
    m ) minor=true;;
    p ) patch=true;;
    d ) dry=true;;
  esac
done

shift $(($OPTIND - 1))

# Display usage
if [ -z $major ] && [ -z $minor ] && [ -z $patch ];
then
  echo "usage: $(basename $0) [Mmp] [message]"
  echo ""
  echo "  -d Dry run"
  echo "  -M for a major release"
  echo "  -m for a minor release"
  echo "  -p for a patch release"
  echo ""
  echo " Example: release -p \"Some fix\""
  echo " means create a patch release with the message \"Some fix\""
  exit 1
fi

# Force to the root of the project
# pushd "$(dirname $0)/../"

# 1) Fetch the current release version

echo "Fetch tags"
git fetch --prune --tags

version=$(git describe --abbrev=0 --tags)
version=${version:1} # Remove the v in the tag v0.37.10 for example

echo "Current version: $version"

# 2) Increase version number

# Build array from version string.

a=( ${version//./ } )

# Increment version numbers as requested.

if [ ! -z $major ]
then
  ((a[0]++))
  a[1]=0
  a[2]=0
fi

if [ ! -z $minor ]
then
  ((a[1]++))
  a[2]=0
fi

if [ ! -z $patch ]
then
  ((a[2]++))
fi

next_version="${a[0]}.${a[1]}.${a[2]}"

username=$(git config user.name)
msg="$1 by $username"

# If its a dry run, just display the new release version number
if [ ! -z $dry ]
then
  echo "Tag message: $msg"
  echo "Next version: v$next_version"
else
  # If a command fails, exit the script
  set -e

  #Creating dockerfile backups
# if [ -z $major ]
# then
#   echo "Creating Dockerfile.$next_version"
#   find . -type f -iname "Dockerfile.build" | while read -r FILE
#   do
#
#     cp  "${FILE}" "${FILE/.build/.$next_version}"
#   done
# fi



  # If it's not a dry run, let's go!


#  change build
if [ -z "$next_version" ]; then
       die "No release tag found; quitting"
       exit 1
fi

if [[ -f  build.yml.template && -f  production.yml.template && -f  django-swarm.yml.template ]]; then
    echo "Releasing version is $next_version"
    sed   "s/RELEASE_TAG/v${next_version}/g" build.yml.template > build.yml
    sed   "s/RELEASE_TAG/v${next_version}/g" production.yml.template > production.yml
    sed   "s/RELEASE_TAG/v${next_version}/g" django-swarm.yml.template > django-swarm.yml
else
    echo "build.yml.template and production.yml.template do not exist "
    exit 1
fi


# 3) Add git tag
   echo "Add git tag v$next_version with message: $msg"


  # 4) Push the new tag

  echo "Push the tag $next_version"
  echo "v$next_version" >> versions
  sed -i "67s/.*/\<p\>v$next_version\<\/p\>/" src/templates/static_pages/about.html
  # Push master
  git add .
  git commit -m "Release version:v$next_version"
  git tag -a "v$next_version" -m "$msg"
  git push  --tags origin $prodBranch

  echo -e "\e[32mRelease done: $next_version\e[0m"
fi



# popd
