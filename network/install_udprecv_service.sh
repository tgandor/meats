#!/bin/bash

service_file=/etc/systemd/system/udprecv.service

if [ -f $service_file ] ; then
    echo "You seem to have it already"
    systemctl status udprecv.service
    exit
fi

udp_recv=$(realpath $(dirname $0)/udp_recv.py)

echo "Setting executable: $udp_recv"

# cat <<EOF
sudo tee $service_file <<EOF
[Unit]
Description=udp_recv.py Service
After=network.target

[Service]
Type=simple
User=pi
ExecStart=$udp_recv -e
Restart=on-abort

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable udprecv.service
sudo systemctl start udprecv.service

