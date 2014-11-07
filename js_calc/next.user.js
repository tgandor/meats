// ==UserScript==
// @name           PrevNext
// @description    Add buttons to navigate to pages with successive numbers.
// @include        http://*
// @version        1.0
// ==/UserScript==

function next(delta)
{
	var match = /\d*$/.exec(window.location.href)[0];
	if (match)
	{
		next_id = parseInt(match) + delta;
		window.location = window.location.href.replace(/\d+$/, next_id);
	}
	else
	{
		alert('Cannot deduce next page.');
	}
}

function make_button(value, left)
{
	var button = document.createElement('input');
	button.type = 'button';
	button.value = value;
	button.style.position = 'fixed';
	button.style.top = 0;
	button.style.left = left;
	document.body.appendChild(button);
	return button;
}

prevButton = make_button('<', 0);
nextButton = make_button('>', '1em');

function make_handler(delta)
{
	return function(e) {
		if (e.which == 2)
		{
			document.body.removeChild(prevButton);
			document.body.removeChild(nextButton);
		}
		else
		{
			next(delta);
		}
	};
}

nextButton.onclick = make_handler(1);
prevButton.onclick = make_handler(-1);
