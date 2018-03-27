#!/bin/bash

# https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
# https://scottlinux.com/2016/09/17/video-stabilization-using-vidstab-and-ffmpeg-on-linux/

ffmpeg_sources=`pwd`
ffmpeg_build=$ffmpeg_sources/build

mkdir -p $ffmpeg_build

if [ -z "$1" ] ; then
num_jobs=`grep processor /proc/cpuinfo | wc -l`
else
num_jobs=$1
fi

if ! which cmake > /dev/null ; then
    sudo apt-get install -y cmake
fi

if ! which hg > /dev/null ; then
    sudo apt-get install -y mercurial
fi

echo Dependencies from APT

# sudo apt-get update

sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev \
  libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev \
  libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev yasm


echo Done

# libx264
sudo apt-get install -y libx264-dev || exit 1

# libx265
hg clone https://bitbucket.org/multicoreware/x265
pushd $ffmpeg_sources/x265/build/linux
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make -j $num_jobs
make install
make distclean
popd

# libfdk-aac
sudo apt-get install -y libfdk-aac-dev || (
	git clone https://github.com/mstorsjo/fdk-aac.git
	pushd fdk-aac/
	time ./configure --prefix="$ffmpeg_build" --disable-shared
	autoreconf -fiv
	make -j $num_jobs
	make install
	make clean
)

# libmp3lame
sudo apt-get install -y libmp3lame-dev || exit 1

# libopus
sudo apt-get install -y libopus-dev || exit 1

# libvpx
if [ ! -f libvpx-1.5.0.tar.bz2 ] ; then
wget http://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.5.0.tar.bz2
fi
tar xjvf libvpx-1.5.0.tar.bz2
pushd libvpx-1.5.0
./configure --prefix="$ffmpeg_build" --disable-examples --disable-unit-tests
make -j $num_jobs
make install
make clean
popd

# vid.stab
git clone https://github.com/georgmartius/vid.stab.git
pushd vid.stab/
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$ffmpeg_build" -DBUILD_SHARED_LIBS:bool=off .
make -j $num_jobs
make install
popd

# ffmpeg
if [ ! -f ffmpeg-snapshot.tar.bz2 ] ; then
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
fi
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$ffmpeg_build/include" \
  --extra-ldflags="-L$ffmpeg_build/lib" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libvidstab \
  --enable-nonfree
  # temporary disabled
  # --enable-libx265 \

make -j $num_jobs
# make install
# make distclean
hash -r
