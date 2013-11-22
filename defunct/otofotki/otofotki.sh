#! /bin/bash

if [ $# -eq 0 ]
then
  echo "Usage: $0 <jpg_file.jpg> [<jpg_file.jpg> ...]"
  echo
  echo "Uploads the image to www.otofotki.pl image hosting service."
  echo "Thumbnail links are then to be found in the file images.html"
  echo "This file should be writable by the user who runs $0"
  exit 1
fi

if ! which curl
then
  echo Missing 'curl' command. Goodbye...
  exit 1
fi

for i in "$@"
do
  echo "<!-- Uploading $i -->"
  curl -s -F "plik1=@$i;type=image/jpeg" http://img30.otofotki.pl/module.php | grep miniaturka | grep -o \<a\ href.\*\</a\> | tee -a images.html
  echo >> images.html
done
