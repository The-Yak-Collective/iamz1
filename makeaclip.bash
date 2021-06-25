#make time a parameter
#make location correct
#make it detect dev2, dev0
#not debugged yet
ffmpeg -y -t 3 -r 25 -i /dev/video0 a_clip.mp4
echo $?
