---
title: Tags and Rss
publish_date: 2025-05-09
is_published: true
slug: tags-and-rss
description: 
tags:
  - short
  - python
---

Hello and welcome back. I plan to make this the final instalment of this python blog series. After which I am free to write about whatever I like, hooray!

## Tags
So, as I plan to begin writing about other various topics, I thought it would be nice to let my (let's be honest, 0) readers know what kind of content would be in a given article. Maybe some people like general dev talk, but don't care about neovim. Or if I ever dip this blog into politics (more when than if), I'm sure some people would want to avoid that like the plague. I can also imagine writing much smaller articles, basically tweets, that could disappoint people that click though expecting more. 

So, I'd like to have a list of "tags" shown on links of my articles, and at the top of my articles. Simple enough!

I added a tags entry to the metadata of my Obsidian markdown files. Since these are a YAML list, my normal find / replace method won't work with these.

There's also the index page where I'm writing a loop in the python build script, then moving that into the page, so I think I have to bite the bullet and make.

## Loops in templates
Welp, I avoided this for as long as I could, but I really should make my templates a bit smarter. Loops at a minimum, bonus points if I can get condition `if - else` blocks working too. 


