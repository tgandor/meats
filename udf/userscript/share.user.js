// ==UserScript==
// @name        ShareThisWithMe
// @namespace   ShareThisWithMe
// @description Sharing pages
// @include     *
// @version     3
// @grant       none
// ==/UserScript==

String.prototype.hashCode = function() {
  var hash = 0, i, chr, len;
  if (this.length === 0) return hash;
  for (i = 0, len = this.length; i < len; i++) {
    chr   = this.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
};

function checkURL(url)
{
	host = url.split('/')[2];
	if (host.hashCode() != 837110838)
		return false;
	return !url.endsWith('=1');
}

if (checkURL(window.location.href))
{
	console.log("Redirecting");
	window.location.replace(window.location.href + '?share=1');
}
