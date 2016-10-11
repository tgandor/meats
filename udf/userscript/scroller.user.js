// ==UserScript==
// @name           AutoScroller
// @description    Add a button which scrolls the page down 10px/s.
// @include        http://*
// @version        1.2
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
scrollButton.onclick = function(e) {
	if (e.which == 2)
	{
		if (this.value == "Stop")
			stopScroll();
		document.body.removeChild(scrollButton);
		return;
	}
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
scrollButton.style.top = '2em';
scrollButton.style.left = 0;
scrollButton.value = 'Scroll';
document.body.appendChild(scrollButton);
