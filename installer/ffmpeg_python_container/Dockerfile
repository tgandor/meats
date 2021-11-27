FROM ubuntu

RUN apt-get update && apt-get upgrade -y
# https://serverfault.com/questions/949991/how-to-install-tzdata-on-a-ubuntu-docker-image
RUN DEBIAN_FRONTEND="noninteractive" TZ="Europe/Warsaw" apt-get install -y ffmpeg python3 python3-opencv python-is-python3 python3-pip
# https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3
RUN pip install tqdm

# https://stackoverflow.com/questions/59904878/docker-compose-volume-name-is-too-short-names-should-be-at-least-two-alphanume
# for manual _work_ this _works_ like this:
# docker run --rm -it -v $(pwd)/:/work ffmpy bash
RUN mkdir /work
WORKDIR /work

# run build from ~/meats as:
# docker build -f installer/ffmpeg_python_container/Dockerfile . -t ffmpy
COPY . /root/meats
