source .env
#INRES="1920x1080" # input resolution
#OUTRES="1920x1080" # output resolution
FPS="15" # target FPS
GOP="30" # i-frame interval, should be double of FPS,
GOPMIN="15" # min i-frame interval, should be equal to fps,
THREADS="2" # max 6
CBR="1000k" # constant bitrate (should be between 1000k - 3000k)
QUALITY="ultrafast"  # one of the many FFMPEG preset
AUDIO_RATE="44100"

#STREAM_KEY="$1" # use the terminal command Streaming streamkeyhere to stream your video to twitch or justin
SERVER="fra02.contribute.live-video.net" # twitch server in frankfurt, see http://stream.twitch.tv/ingests to change

ffmpeg -re -f v4l2 -i /dev/video0 \
-c:v libx264 -preset veryfast -maxrate 1000k \
-bufsize 500k -r 10 -tune zerolatency -pix_fmt yuv420p -g 50 -an \
-f flv "rtmp://$SERVER/app/$STREAM_KEY"
#ffmpeg -f x11grab -s "$INRES" -r "$FPS" -i :0.0 -f alsa -i pulse -f flv -ac 2 -ar $AUDIO_RATE \
#-vcodec libx264 -g $GOP -keyint_min $GOPMIN -b:v $CBR -minrate $CBR -maxrate $CBR -pix_fmt yuv420p\
#-s $OUTRES -preset $QUALITY -tune film -acodec libmp3lame -threads $THREADS -strict normal \
#-bufsize $CBR "rtmp://$SERVER.twitch.tv/app/$STREAM_KEY"


