#!/bin/bash
#make time a parameter
#make location correct
#detect dev2, dev0 (using error, maybe)
#mpeg -> mp4 is probably not best way
ffmpeg -hide_banner -loglevel error -y -t 3 -i /dev/video0 a_clip.mpeg
echo $?
if [ $? -gt 0 ]
then
    ffmpeg -hide_banner -loglevel error -y -t 3 -i /dev/video2 a_clip.mpeg
    echo $?
fi
ffmpeg -y -i a_clip.mpeg  -c:v libx264 a_clip.mp4
