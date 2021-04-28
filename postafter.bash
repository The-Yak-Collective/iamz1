post_file=$(mktemp)
echo "trying to post after prog stopped" $1 $YAK_ROVER_NAME >trackingfile
echo '{"wait": true, "content": "' $YAK_ROVER_NAME ': lets try to upload a results file ' $1 '"}'>$post_file
#echo $1 >>$post_file
#echo '"}' >>$post_file
sed -i 's/$/\\n/' $post_file
sed -i '$s/..$//' $post_file
astring=$(<$post_file)
echo $astring
curl -i -H 'Expect: application/json' -F file=@$1 -F "payload_json=${astring}" $TWEAKS_HOOK