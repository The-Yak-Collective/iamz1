#!/bin/bash
echo "starting command" $0
pwd
temp_file=$(mktemp) #i am actually NOT sending the output yet
mess_file=$(mktemp)
source "$@" >temp_file 2>&1 &
export APP_PID=$! 
echo '{"content": "' >mess_file
echo 'pid is' $APP_PID >>mess_file
echo '"}' >>mess_file
sed -i 's/$/\\n/' mess_file
sed -i '$s/..$//' mess_file
curl -d "@mess_file" -H "Content-Type: application/json" -X POST $TWEAKS_HOOK 