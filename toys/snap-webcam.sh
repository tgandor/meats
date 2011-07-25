subdir=`date +'%Y-%m-%d_%H-%M-%S'`
mkdir $subdir
cd $subdir
mplayer -vo jpeg -frames 75 -fps 30 -tv driver=v4l2:width=640:height=480:device=/dev/video0 tv://
echo "Frames stored in $subdir"

