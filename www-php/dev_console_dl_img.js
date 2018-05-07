// select all images ($ == jquery)

$('img')

// print image URLs

$('img').each(function(x)  { console.log(x, this.src); })

// download image by link

var a = $("<a>")
    .attr("href", "http://i.stack.imgur.com/L8rHf.png")
    .attr("download", "img.png")
    .appendTo("body");

a[0].click();

a.remove();

// download all images;


$('img').each(function(x)  {
    var url = this.src;
    if (!url.endsWith('.jpg')) return;
    console.log(x, this.src);
    var a = $("<a>")
        .attr("href", this.src)
        .attr("download", "")
        .appendTo("body");

    a[0].click();

    // a.remove();
})

(actually, downloaded only the first!)


// this works around this - run this, then repeat: download_files(downloads)

var downloads = [];

$('img').each(function(x)  {
    var url = this.src;
    if (!url.endsWith('.jpg')) return;
    console.log(x, this.src);
    var a = $("<a>")
        .attr("href", this.src)
        .attr("download", "")
        .appendTo("body");
    downloads.push(a[0]);
    a[0].click();
})

function download_files(downloads) {
    var l = downloads.pop()
    window.setTimeout(1000, function() { download_files(downloads); }); // doesn't work
    
    l.click()
}

// whitelisting the page didn't help
// further experiments will be done as needed.
