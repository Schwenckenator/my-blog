---
title: Introducing FloatNote.nvim
publish_date: 2026-02-18
is_published: true
slug: floatnote-nvim
description: My tiny neovim plugin for taking quick notes
tags:
  - neovim
  - personal
---

## FloatNote!
I have made a tiny plugin, and released it on codeberg. Here it is!

[floatnote.nvim](https://codeberg.org/Schwenckenator/floatnote.nvim)

## What does it do?
Very simply, it allows you to open a file in a floating window, write down some quick notes, and have
that file auto save, and re-open when you open the window in the same project (more specifially, the `cwd`).

You use the command `:FloatNote` to open and close the window, but <kbd>Esc</kbd> in normal mode will
also close the window, and automatically save the file.

No more opening up a scratch buffer, finding somewhere to save it without messing with `.gitignore`!

## Why should I use it?
You almost definitely shouldn't.

Now that's a weird thing to say from someone spruiking about making a plugin. But I would suggest,
for a plugin this simple, this is something anyone could, _and should_, write for themselves.

It is incredibly easy to start writing Neovim plugins. Because it's exactly the same as writing your
own config, just with code that other people can use too. Users of _other editors_, unfortunately don't
have such an easy time writing custom plugins. It's precisely because Neovim uses Lua (fantastic language btw)
and the configuration language is the same as writing plugins, that I would encourage every developer
that uses Neovim to write some plugins and share them.

## Ways to improve FloatNote?
There are so many things I could do. I could add configurable settings, I could make it save notes
based on git repo, or git branch. But I probably won't do those, at least they aren't a priority.

One thing I am curious about though, is attaching notes to files in the project using virtual text.
Sometimes during my work, I want a special note just for me, but writing a comment will change the code
for everyone. So If I could have parts of this global note, displaying virtual text in the code, I think
that would be pretty cool.

Anyway, that's all for this post. Have a dig through my code! It's probably awful, so feel free to reach
out on my socials and tell me how to improve it!
