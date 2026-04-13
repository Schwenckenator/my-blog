---
title: Massive Update
publish_date: 2026-04-13
is_published: true
slug: massive-update
description: Added a bunch of new pages
tags:
  - build-a-blog
  - personal
  - javascript
---
## New pages!
I have knuckled down and added a few new pages to this site, trying to integrate it more into the personal web.

From my previous todo list, I have added a personal stuff page, and a links page.
The links page is still a bit anaemic, but I plan to add more when I find more cool indie sites!

On that links page, I've added my own 88x31 badge, and a little button that copies the html to your clipboard.
And I put this javascript, in true Locality of Behaviour fashion, directly into the page where it is needed!

<h4>My Badge!</h4>
<article id="my-badge">
	<a href="https://schwenckenator.dev">
		<img alt="schwenckenator.dev" width="88" height="31" src="https://schwenckenator.dev/img/badge.gif">
	</a>
</article>

Here is the entirety of my badge, and the copy code.

```html
<h3>My Badge!</h3>
<article id="my-badge">
	<a href="https://schwenckenator.dev"><img alt="schwenckenator.dev" width="88" height="31"
			src="https://schwenckenator.dev/img/badge.gif"></a>
	<button id="badge-copy-button">Copy</button>
	<script>
		document.querySelector("#badge-copy-button").addEventListener("click", () => {
			const badgeSection = document.querySelector("#my-badge").children;
			const badgeHtml = badgeSection.item(0).outerHTML;
			navigator.clipboard.writeText(badgeHtml);

			const btn = document.querySelector("#badge-copy-button")
			btn.innerHTML = 'Copied!!'
			setTimeout(() => {
				btn.innerHTML = 'Copy'
			}, 3000)
		});
	</script>
</article>
```
So when you click my button, this script fires. I didn't want to have html for the display badge,
and a separate html in the javascript for the copying. So I pull the html from the page itself with this.

```js
const badgeSection = document.querySelector("#my-badge").children;
const badgeHtml = badgeSection.item(0).outerHTML;
navigator.clipboard.writeText(badgeHtml);
```

That gets the html from the `my-badge` id, which is the `<article>` tag that surrounds the whole thing.
I get the first child (which I know is the badge I want, I build the site) and put its HTML into a variable.
Then simply write it to the clipboard!

Next, because there is no feedback whatsoever that the code has been copied, I change the button text for 3 seconds.

```js
const btn = document.querySelector("#badge-copy-button")
btn.innerHTML = 'Copied!!'
setTimeout(() => {
	btn.innerHTML = 'Copy'
}, 3000)
```

Really easy, I get the button element by id. Change the text with `innerHTML`. Then start a timeout to turn it back.

Javascript really isn't so bad once you're not relying on it for everything.

Anyway, check out my new pages in the header or here!
<ul>
	<li>
		<a href="/my-stuff">My Stuff</a>
	</li>
	<li>
		<a href="/links">Links</a>
	</li>
</ul>
