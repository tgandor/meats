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

// (actually, downloaded only the first!)


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
    // a[0].click();
})

function download_files_1_new(downloads) {
    let link = downloads.pop();
    link.click();
    setTimeout(function() { download_files_1_new(downloads); }, 500);
}

// https://stackoverflow.com/questions/14033588/javascript-click-method-only-works-once-in-chrome-extension

function download_files2(downloads) {
    downloads.forEach(element => {
        console.log(element.href);
        element.click();
    });
}

download_files(downloads)

javascript:download_files2(downloads)

// whitelisting the page didn't help
// further experiments will be done as needed.

function clicker(el, clickCount = 1) {
    var mousedownEvent;
    while(clickCount--) {
      mousedownEvent = document.createEvent("MouseEvent");
      mousedownEvent.initMouseEvent("click", true, true, window, 0, null, null, null, null, false , false, false, false, 0, null);
      el.dispatchEvent(mousedownEvent);
    }
  }

function download_files3(downloads) {
    downloads.forEach(element => {
        console.log(element.href);
        clicker(element, 1)
    });
}

function download_files4(downloads) {
    downloads.lengt
    downloads.slice()
    var mousedownEvent =  document.createEvent("MouseEvent");
    mousedownEvent.initMouseEvent("click", true, true, window, 0, null, null, null, null, false , false, false, false, 0, null);
    downloads.forEach(element => {
        console.log(element.href);
        element.dispatchEvent(mousedownEvent);
    });
}


function download_files5(downloads, timeout=1500) {
    if (downloads.length == 0) return;

    var mousedownEvent =  document.createEvent("MouseEvent");
    mousedownEvent.initMouseEvent("click", true, true, window, 0, null, null, null, null, false , false, false, false, 0, null);
    downloads[0].dispatchEvent(mousedownEvent);
    window.setTimeout(function() { download_files5(downloads.slice(1), timeout); }, timeout);
}

(function() { download_files5(downloads); })();

// 500 ms is a reasonable timeout.

// simple download (if your page is whitelisted... I guess.)

(function() {
    var downloads = [];

    $('img').each(function(x)  {
        var url = this.src;
        if (!url.endsWith('.jpg')) return;

        console.log(x, 'Adding: ' + this.src);
        var a = $("<a>")
            .attr("href", this.src)
            .attr("download", "")
            .appendTo("body");
        downloads.push(a[0]);
    })

    function download_files_1_new(downloads) {
        if (downloads.length == 0) return;

        let link = downloads.pop();
        console.log('Downloading: ' + link.href);
        link.click();
        setTimeout(function() { download_files_1_new(downloads); }, 2000);
    }

    download_files_1_new(downloads);
})();
