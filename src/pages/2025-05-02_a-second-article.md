sina lukin e ni la, sina pona a!

Welcome back, I'm still working on my static site generator / blog. This time I'll try and fix my codeblocks, and get a homepage with both of my posts on it done! Bonus points if I can make previous / next links in the articles themselves.

## Codeblocks

So with the default markdown converter in python, my Obsidian markdown got absolutely mangled. The backtick syntax "\`\`\`" wasn't recognised, so the contents of those codeblocks were interpreted as real HTML, which was a disaster.

I had to first convert all of the HTML special symbols `<>"` into their safe counterparts `&lt; &gt; &quot;`, then because of my neovim's automatic formatting, I had to manually position the whitespace in the blocks to look right in the final HTML.

As I said, disaster. I maybe could have worked out how to turn off my formatter temporarily, but I just wanted to finish and get something published. I'll just put a toggleable auto-format on my todo-list when I rewrite my config next.


