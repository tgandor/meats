// ==UserScript==
// @name           AutoScroller
// @description    Add a button which scrolls the page down 10px/s.
// @include        *
// @version        1.1
// ==/UserScript==


function pageScroll()
{
	// horizontal and vertical scroll increments
	scrollBy(0, 1);
	// scrolls every 100 milliseconds
	scrolldelay = setTimeout(pageScroll, 100);
}


function stopScroll()
{
	clearTimeout(scrolldelay);
}

scrollButton = document.createElement('input');
scrollButton.type = 'button';
scrollButton.onclick = function() {
	if (this.value == "Scroll")
	{
		pageScroll();
		this.value = "Stop";
	}
	else
	{
		stopScroll();
		this.value = "Scroll";
	}
};
scrollButton.style.position = 'fixed';
scrollButton.style.top = 0;
scrollButton.style.left = 0;
scrollButton.value = 'Scroll';
document.body.appendChild(scrollButton);
window.scrollButton = scrollButton;
