#!/bin/bash
export SSHPASS=$DEPLOY_PASS
sshpass -e ssh $DEPLOY_USER@$DEPLOY_HOST "sh $DEPLOY_PATH/web/minideploy.sh"