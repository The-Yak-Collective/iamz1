post_file=$(mktemp)
echo "trying to post after prog stopped" $1
echo '{"content": "lets try to upload a results file ' >$post_file
echo $1 >>$post_file
echo '"}' >>$post_file
sed -i 's/$/\\n/' $post_file
sed -i '$s/..$//' $post_file
astring=$(<$post_file)
echo $astring
curl -i -H 'Expect: application/json' -F file=@$1 -F "payload_json=${astring}" $TWEAKS_HOOK