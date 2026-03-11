---
title: C... is hard
publish_date: 2026-03-11
is_published: true
slug: c-is-hard
description: 
tags:
  - build-a-blog
  - personal
---

## So where is that site rewrite in C?
Yeah, who knew, C is a hard language.

I have been otherwise preoccupied, but I have had a decent crack at a blog-builder in C.
I was able to walk the site directory recursively, and was able to print the path of all files found.
That was pretty cool.

From my experience over the past couple of weeks, programming in C feels like driving a manual car.
It's more involved, obviously, but you do feel more in control of the machine. 
Programming in C felt like programming a computer, rather than a magic box that follows instructions,
a la javascript.

And that's all well and good, but I hit a problem as soon as I tried to interpret the frontmatter of the blogs markdown files.
The problem being, I don't know shit about how to properly manage memory.
I had segfaults for days. Strings in C are hard.

So, after a long night hunting pointer errors, I thought to myself. 
This is not a valuable use of my limited "kids' asleep" time.

## You're giving up?
Not exactly, C is just going to go on the back burner for a bit.
Even if I did completely shelve it, I still learnt a lot, so I don't consider the time wasted.

However, my goal was to update my site, to make in more in-line with my vision for joining the indie-web.
And spending months fart-arsing around in C while the site remains frozen was not what I had in mind.

## The new plan
I'll stick with python for now. But I did come up with a good idea when preparing for the C rewrite.
I'm going to generalise the templating logic somewhat, to allow for pages other than just blog posts.

```
.
├── site
│   ├── about
│   │   └── index.html
│   ├── blog
│   │   ├── 2026_6-blog-page.md
│   │   └── template.html
│   ├── css
│   │   ├── code.css
│   │   ├── index.css
│   │   └── pico.jade.min.css
│   ├── img
│   │   └── my-images.png
│   ├── index.html
│   ├── rss-template.xml
│   └── template.html
└── src
	└── main.c
```

Here we have an example of the file tree. \
First, only the code that builds the site lives in `src`.
The actual pages of the website have been moved to a new `site` folder.
Also, rather than hard coding the homepage and blog pages templates, I have removed the `templates` folder,
and instead put in `template.html` amongst the other files.

I'm hoping to harness the file tree, and have nested templates working for each page.

I could go into more detail, but this idea is not yet battle tested, so I'd much rather have a crack at it,
and report back once I've made some progress!

### A quick aside
I am going to break, like, all of the links on this page when this drops. For future proofing purposes,
I'm going to move the blog pages under the `blog/` path, which if bookmarked now, will return 404s later.
I promise this will be the first, and last, time I do something like this. 
After all, [Cool URLs don't change](https://www.w3.org/Provider/Style/URI).

## What about C?
I still have ideas for learning C. I think I need to first just get some experience writing C, so I 
plan on implementing clox from [Crafting Interpreters](https://craftinginterpreters.com/).
I have used this book as a basis for creating my own language "speel" in gdscript, but I think I'll
just follow the book to get a handle on C. Maybe I'll make "cSpeel" if I'm feeling fancy.

But, once that's done, I have a really dumb idea to make a markup language to replace HTML, CSS, and 
maybe even javascript, but that will have to wait until another day.
