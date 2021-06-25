#make time a parameter
#make location correct
#make it detect dev2, dev0 (using error, maybe)
#not debugged yet
ffmpeg -hide_banner -loglevel error -y -t 3 -r 25 -i /dev/video0 a_clip.mp4
echo $?
ffmpeg -hide_banner -loglevel error -y -t 3 -r 25 -i /dev/video2 a_clip.mp4
echo $?
