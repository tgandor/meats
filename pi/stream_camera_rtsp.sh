#!/bin/bash

screen -S streaming -dm bash -c "raspivid -o - -t 0 -hf | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8554/x}' :demux=h264"

echo "Streaming in screen session 'streaming'"
echo "To kill (stop streaming) run:"
echo
echo "screen -S streaming -X quit"
echo
echo "To attach and see output:"
echo
echo "screen -r streaming"
echo

echo "Streaming URLs:"
ifconfig | awk '/inet addr:/ { print $2 }' | sed 's/addr://' | while read ip; do
    echo "rtsp://$ip:8554/x"
done
