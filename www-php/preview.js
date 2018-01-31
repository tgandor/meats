
// cheat sheets used:
// https://developer.mozilla.org/en-US/docs/Learn/Server-side/Node_server_without_framework
// https://javascript.info/promise-chaining#returning-promises

var http = require('http');
var fs = require('fs');
var path = require('path');

var port = 8080
var header = '';
var footer = '';

var promises = [
    new Promise(function(resolve, reject) {
        fs.readFile('_header.html', function(error, content) {
            if (error) {
                console.log('_header.html not present')
            } else {
                header = content;
            }
            resolve();
        });
    }),
    new Promise(function(resolve, reject) {
        fs.readFile('_footer.html', function(error, content) {
            if (error) {
                console.log('_footer.html not present')
            } else {
                footer = content;
            }
            resolve();
        });
    })
]

Promise.all(promises).then(function() {

http.createServer(function (request, response) {
    console.log('request ', request.url);

    var contentType = 'text/html';

    // if (filePath == './') {
    //    filePath = './index.html';
    // }

    // print directory index instead:
    if (request.url == '/') {
        new Promise(function(resolve, reject) {
            response.writeHead(200, { 'Content-Type': contentType });
            response.write('<html><head><title>Index</title></head><body>\n');
            resolve(response);
        }).then(function(response) {
            return new Promise(function(resolve, reject) {
                fs.readdir('.', function(err, files) {
                    if (err) {
                        console.log('fs.readdir error: ' + err)
                    } else {
                        files.forEach(function (name) {
                            response.write('<a href="' + name + '">' + name + '</a><br />\n');
                        });
                    }
                    resolve(response);
                });
            });
        }).then(function(response) {
            response.write('</body></html>\n');
            response.end();
        });
        return;
    }

    var filePath = '.' + request.url;

    var extname = String(path.extname(filePath)).toLowerCase();

    // not used
    var mimeTypes = {
        '.html': 'text/html',
        '.js': 'text/javascript',
        '.css': 'text/css',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.gif': 'image/gif',
        '.wav': 'audio/wav',
        '.mp4': 'video/mp4',
        '.woff': 'application/font-woff',
        '.ttf': 'application/font-ttf',
        '.eot': 'application/vnd.ms-fontobject',
        '.otf': 'application/font-otf',
        '.svg': 'application/image/svg+xml'
    };

    // contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, function(error, content) {
        if (error) {
            if(error.code == 'ENOENT'){
                fs.readFile('./404.html', function(error, content) {
                    response.writeHead(200, { 'Content-Type': contentType });
                    response.end(content, 'utf-8');
                });
            }
            else {
                response.writeHead(500);
                response.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
                response.end();
            }
        }
        else {
            response.writeHead(200, { 'Content-Type': contentType });
            response.end(header + content + footer, 'utf-8');
        }
    });

}).listen(port);

console.log('Server running at http://127.0.0.1:' + port + '/');

});

