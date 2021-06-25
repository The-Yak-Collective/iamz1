#!/bin/bash
#make time a parameter
#make location correct
#detect dev2, dev0 (using error, maybe)
#mpeg is probbaly not best way
ffmpeg -hide_banner -loglevel error -t 3 -i /dev/video0 a_clip.mpeg
echo $?
if [$> -gt 0]
then
    ffmpeg -hide_banner -loglevel error -t 3 -i /dev/video2 a_clip.mpeg
    echo $?
fi
