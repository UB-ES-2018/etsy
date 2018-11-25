#!/bin/bash
export SSHPASS=$DEPLOY_PASS
sshpass -e ssh $DEPLOY_USER@$DEPLOY_HOST $DEPLOY_PATH/web/minideploy.sh