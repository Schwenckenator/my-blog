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

I'm going to take some inspiration from Svelte here, and call it an each block. To make things easier, I decided to repeat the key at the start and end of the block.
```html
{{ #each key }}
<!-- each block content -->
{{ /each key }}
```

With this, I can parse the template using regex, and I don't need to do any open / close counting.

I rewrote my home page link template like so:
```html
    <main>
        <section class="container">
-           <!-- {{ content }} -->
+           {{ #each pages }}
+           <article>
+               <hgroup>
+                   <div class="grid">
+                       <h4>
+                           <a class="contrast" href="/{{ slug }}">
+                               {{ title }}
+                           </a>
+                       </h4>
+                       <p class="to-end">{{ publish_date }}</p>
+                   </div>
+                   <p>
+                       <small>
+                          {{ description }}
+                       </small>
+                   </p>
+               </hgroup>
+               <footer>
-                   <!-- {{ tag_list }} -->
+                   {{ #each tags }}
+                   <code>#{{ . }}</code>
+                   {{ /each tags }}
+               </footer>
+           </article>
+           {{ /each pages }}
        </section>
    </main>
```

And to render these blocks, I wrote a each block render function!
```python
def replace_template_each(each_key, data_list, template):
    """replaces a list block"""

	each_start = f"{{{{ #each {each_key} }}}}"
    each_end = f"{{{{ /each {each_key} }}}}"
    regex = fr"{each_start}(.*?){each_end}"

    matches = re.search(regex, template, re.S)
    each_block = ""


    if matches:
        each_block = matches.group(1)
    else:
        return template

    content = ""
    result = template

    for data in data_list:
        item = each_block
        if isinstance(data, dict):
            item = template_replace(data, item)
        else:
            item = template_replace({'.': data}, item)
        content += item + "\n"

	# 
    result = re.sub(regex, content, template, flags=re.S)

    return result

```

Now this works for the each blocks, but unfortunately it leaves the empty blocks behind. And I get the feeling that I'm coming at this problem from the wrong direction. So I think it's time to do a template rewrite.

## Rewriting my template engine
Up until now, I've been looping over the pages metadata, or other dictionary, and replacing any tags that are found. But that feels backwards to me now, and I don't think it would play nice with `if` blocks. So I'm flipping the script, I'm going to scan the template for keys, then replace them with data, or delete it if the data isn't found.

Because the order of operations is highly important, I'll make sure to replace each key in order which they are found in the document. 