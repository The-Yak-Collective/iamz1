mess_file=$(mktemp)
echo "trying to post after prog stopped"
echo '{"content": lets try to upload a results file "' >$mess_file
echo $1 >>$mess_file
#echo 'pid is' $APP_PID >>$mess_file
echo '"}' >>$mess_file
sed -i 's/$/\\n/' $mess_file
sed -i '$s/..$//' $mess_file
curl -i -H 'Expect: application/json' -F file=@$1 -F 'payload_json=@$mess_file' $TWEAKS_HOOK