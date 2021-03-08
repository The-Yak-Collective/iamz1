#!/bin/bash
echo "starting command" $0
echo "parameters" "$@"
echo "the working directory is"
pwd
temp_file=$(mktemp) #i am actually NOT sending the output yet
mess_file=$(mktemp)
source "$@" >$temp_file 2>&1 && /bin/bash postafter.bash $temp_file &
export APP_PID=$! 
echo '{"content": "' >$mess_file
echo 'pid is' $APP_PID >>$mess_file
echo '"}' >>$mess_file
sed -i 's/$/\\n/' $mess_file
sed -i '$s/..$//' $mess_file
curl -s -d "@$mess_file" -H "Content-Type: application/json" -X POST $TWEAKS_HOOK 