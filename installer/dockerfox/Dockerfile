# based on creack/firefox-vnc
# https://stackoverflow.com/a/16311264/1338797

FROM ubuntu as intermediate
# intermediate image thanks to:
# https://vsupalov.com/build-docker-image-clone-private-repo-ssh-key/
# CAUTION!!! the intermediate image stays in `docker image list`
# (without name, but with a hash)
# to prevent `docker history <intermediate_hash>` from seeing ARG
# do `docker image rm <intermediate_hash>` after building.

RUN     apt-get update
RUN     apt-get install -y x11vnc
RUN     mkdir ~/.vnc

# Setup a password
ARG     VNC_PASS=1234
RUN     x11vnc -storepasswd $VNC_PASS ~/.vnc/passwd

FROM ubuntu

RUN     apt-get update
RUN     apt-get upgrade

RUN     apt-get install -y x11vnc xvfb firefox
RUN     mkdir ~/.vnc

COPY --from=intermediate /root/.vnc/passwd /root/.vnc/passwd

# Autostart firefox (might not be the best way to do it, but it does the trick)
RUN     bash -c 'echo "firefox" >> /.bashrc'

# With help from: https://docs.docker.com/engine/reference/builder/

EXPOSE 5900
CMD    ["x11vnc", "-forever", "-usepw", "-create"]
