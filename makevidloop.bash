#install apt-get v4l2loopback-dkms  - see https://github.com/umlaeute/v4l2loopback and then   https://github.com/umlaeute/v4l2loopback/wiki/FFmpeg
sudo modprobe v4l2loopback exclusive_caps=1
nohup ffmpeg -hide_banner -loglevel error -re -i /dev/video0 -f v4l2 /dev/video2 