
function unzipd {
    unzip "$1" -d `basename "$1" .zip`
}
