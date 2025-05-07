---
title: "The start of my blog"
publish_date: 2025-04-26
is_published: true
slug: 'start-of-blog'
description: "As I'm starting to get older, I'm having more and more opinions about all sorts of things. And considering the stranglehold big tech companies have on social media, the best way I think to get my thoughts out there, will be my very own site!..."
---
As I'm starting to get older, I'm having more and more opinions about all sorts of things. And considering the stranglehold big tech companies have on social media, the best way I think to get my thoughts out there, will be my very own site!

I don't expect to be famous, or have anyone read this at all really. But I want to use this site as a record of my personal projects, and also to be the impetus to actually make those projects.

These are the goals I'm setting out for this site.
- I want it to be dead simple to use
- I want to write my articles in markdown
- I want my article list, or previous / next links to be generated automatically.

To accomplish this, I'm going to avoid using fancy JavaScript frameworks and static site generators. I don't want to deal with databases, or any server nonsense.

I think this can be a learning opportunity, so I'm going to write a static site generator from scratch using (probably?) python. 

## Getting started

To start though, I just need to get html onto a server. I've gotten myself this domain [https://schwenckenator.dev](https://schwenckenator.dev) from cloudflare, and I'm going to use their pages service to serve my static html.

I whipped up a public [GitHub repository](https://github.com/Schwenckenator/my-blog) where I'll keep this site's code. 
Next, I deployed it using [cloudflare's guide here](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/). It was really quite simple! 


![My first build error](first-build-error.png)

But, I got my first error! I need to put something into the build folder.

Using the "ship it now, make it good later" philosophy, I simply shoved a hello world template into the build folder, and pushed it!

![My first build success!](first-build-success.png)

Success!

## Actually making the site
So, I'm not much of a web designer. My day job (using Next/React, blegh) has me fully focused on the interactivity, and the css gets passed onto the designers. 

However, I also want this site to look *okay*. So, I've enlisted the help of [picocss](https://picocss.com/)!
After playing with tailwind before, I find it can get kinda bloaty with the classes, and I'm avoiding build steps where I can, so a css framework is perfect. I also just like the look of picocss. 

Next, I need to actually write the html for this sites pages. I think later I'll rewrite these as a template, but for now, I'm happy with just hard-coding the html and pushing it into the build folder. 

After futzing a bit, I've made my first draft of my main page! I've taken inspiration from [https://qwool.github.io/](https://qwool.github.io/), I think its a nice simple place to start.

```html
<!doctype html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark">
    <link rel="stylesheet" href="css/pico.jade.min.css">
    <link rel="stylesheet" href="css/index.css">
    <title>Hello world!</title>
</head>

<body>
    <header>
        <div class="container">
            <h5>
                Schwenckenator.dev
            </h5>
            <div>
                <small>
                    Thoughts on personal projects, neovim, languages, and anything else that crosses my mind
                </small>
            </div>
            <div>
                <a href="#" class="secondary">
                    Home
                </a>
            </div>
        </div>
    </header>
    <main>
        <section class="container">
            <h1>Hello world!</h1>
            <p>
                ni li lipu nanpa wan a!
                <br>
                tenpo kama la, mi sitelen insa ni
            </p>
        </section>
    </main>
    <footer class="container">
        <div>
            Find me elsewhere!
        </div>
        <section>
            <a href="https://github.com/Schwenckenator/">
                GitHub
            </a>
            /
            <a href="https://bsky.app/profile/schwenckenator.bsky.social">
                Bluesky
            </a>
            /
            <a href="https://aus.social/@Schwenckenator">
                Mastodon
            </a>
        </section>
    </footer>
</body>

</html>
```

This has got everything I really need for now. A place to put my articles, and a simple header and footer. 

I'll want to add <-prev / next -> links too, but I can do that once I actually have multiple articles to show. 

I'll also have to make the home page a list at some point. So much left to do!

## My first build step
Now, it's time to write some actual code. 
At the moment, I'm uploading the build folder to git directly. But I'd rather have the build folder be ignored by git, and have cloudflare build my project on deployment. 

Since there is no actual build step for the site yet, for now I think I can get away with copying a source directory to the build directory like so:
```bash
cp -r ./src ./build
```

Later, when the site actually has a build step, I'll have to convince cloudflare to run a python script. 

## Finishing up this article
So far, I've been writing this article in Obsidian, outside of the repo. So as a final step, I need to move this markdown file into the repo, and run a python script on it to convert it to HTML.

I installed the markdown package with pip
```bash
pip install markdown
```

And tested it out with the interactive REPL
```python
>>> import markdown
>>> markdown.markdown("# Hey Mum")
'<h1>Hey Mum</h1>'
```

Satisfied that this works, I wrote a small terminal script that loads the file from the first argument, and spits the result out into the second.

First I checked that I could read terminal arguments
```python
import sys

print(sys.argv)

# Input "python3 convert.py first second third"
# Output ['convert.py', 'first', 'second', 'third']
```

Then I put the code to convert the file, and let her rip!
(With lots of printing, because I can.) 
```python
import markdown
import sys

read_path = sys.argv[1]
write_path = sys.argv[2]

if not read_path or not write_path:
    print('Arg 1 is read path, Arg 2 is write path')
    return

with open(read_path, 'r') as f:
    text = f.read()
    print('Markdown:')
    print(text)
    html = markdown.markdown(text)
    print('HTML:')
    print(html)

with open(write_path, 'w') as f:
    f.write(html)
```

And I got an error!
```
  File "/home/matt/projects/my-blog/convert.py", line 9
    return
    ^^^^^^
SyntaxError: 'return' outside function
```

So I swapped the `if .. return` for a couple of `assert` statements

```python
import markdown
import sys

read_path = sys.argv[1]
write_path = sys.argv[2]

assert read_path, "Read file path and write file path not included!"
assert write_path, "Write file path not included!"

with open(read_path, 'r') as f:
    text = f.read()
    print('Markdown:')
    print(text)
    html = markdown.markdown(text)
    print('HTML:')
    print(html)

with open(write_path, 'w') as f:
    f.write(html)
```

And it works! I mean, I got an output file at least. There's still a lot of work cleaning it up, but it's better than nothing!

## Thoughts
So, all I've got left to do is put finish writing this article, put it through my converter, clean it up, and publish!

> I'm writing this after conversion, directly into the HTML. So the next order
> of business is working out how to make the converter not mangle my code
> blocks, because that took a ***lot*** of work to fix.

After that, I think I want to make my python script crawl through the pages
folder, converting all of the files, and saving the html to the build folder.
I'll also need to make the index page a list of all my articles. At the moment,
this is all I've got, so homepage it is!

I could also work on automatically building links in, but I want to chip away
at this project, slowly building it up so I don't burn out. And once I'm in the
groove of writing a post every week or so, maybe I'll start working on games,
or another tool after finishing this.

Until next time,\
pona tawa sina! mi tawa.
