#!/bin/bash

pushd `dirname $0`

python ../system/systemd_wrap.py ../network/udp_recv.py -e | sudo tee /etc/systemd/system/udprecv.service

sudo systemctl enable udprecv
sudo systemctl start udprecv

popd
