#!/bin/bash
ACTION='\033[1;90m'
FINISHED='\033[1;96m'
READY='\033[1;92m'
NOCOLOR='\033[0m' # No Color
ERROR='\033[0;31m'
echo
echo -e ${ACTION}Checking Git repo
echo -e =======================${NOCOLOR}
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "DEPLOY" ]
then
  echo -e ${ERROR}Not on deploy. ${NOCOLOR}
  echo
  exit 0
fi
git fetch
HEADHASH=$(git rev-parse HEAD)
UPSTREAMHASH=$(git rev-parse DEPLOY@{upstream})
if [ "$HEADHASH" != "$UPSTREAMHASH" ]
then
  echo -e ${ERROR}Not up to date with origin - pulling changes.${NOCOLOR}
  echo -e ${ACTION}=======================${NOCOLOR}
  git pull
  echo -e ${ACTION}=======================${NOCOLOR}
  echo -e  ${FINISHED}Pulled all changes! Up to date!${NOCOLOR}
  echo -e ${ACTION}=======================${NOCOLOR}
  echo -e ${ACTION}Rebuilding the containers
  docker-compose build
  docker-compose up -d
  echo -e  ${FINISHED}Containers builded${NOCOLOR}
  echo -e ${ACTION}=======================${NOCOLOR}
  echo -e ${ACTION}Migrating DB
  docker exec etsy_web_1 /bin/sh -c "cd etsy && python3 manage.py migrate"
  echo -e  ${FINISHED}Database migrated${NOCOLOR}
else
  echo -e ${FINISHED}Current branch is up to date with origin/master.${NOCOLOR}
fi