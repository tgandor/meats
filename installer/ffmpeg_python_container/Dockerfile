FROM ubuntu

RUN apt-get update && apt-get upgrade -y
RUN DEBIAN_FRONTEND="noninteractive" TZ="Europe/Warsaw" apt-get install -y ffmpeg python3 python3-opencv \
    python-is-python3 python3-pip python3-tqdm pipx

# docker run --rm -it -v $(pwd)/:/work ffmpy bash
RUN mkdir /work
WORKDIR /work

# run build from ~/meats as:
# docker build -f installer/ffmpeg_python_container/Dockerfile . -t ffmpy
COPY . /root/meats
