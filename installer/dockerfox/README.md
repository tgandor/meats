# Firefox + VNC in a container

This builds on ubuntu, updates the system, and installs firefox.
Then it enables using VNC for connecting with the container.

## Local build + running

First build the container, specifying password if necessary:

`$ docker build . [--build-arg VNC_PASS=your_passw0rd] -t dockerfox`

Then, run the container:

`$ docker run -P -d dockerfox`

You need -P to have a random port exposed. You can also expose the default port:

`$ docker run -p 5900:5900 -d dockerfox`

You may also go somewhat more secure, because using e.g. -ssl TMP doesn't work
with some clients (e.g. vinagre).

So better run this just like that:

`trustedhost $ docker run -d dockerfox`

And then:

`ssh -L 5900:172.xx.xx.2:5900 user@tustedhost`

where "172.xx.xx.2" is the IP of the container in the docker networking, and connect to VNC via localhost. 
