---
title: I got stuck
publish_date: 2026-02-16
is_published: true
slug: i-got-stuck
description: I suffered a major case of programmers block, but I think I have a solution
tags:
  - game-dev
  - personal
---

## So I got stuck

I got stuck. I was having trouble working out how the attacking system would work. 
I was trying to have it animate programmatically, and I just couldn't work out how to have the 
hand and sword properly rotated during an attack.

Not to mention, kids not sleeping properly, and prepping my "Draw Steel!" game, (and Terraria 1.4.5 dropping)
I just didn't have the energy for game dev. 

I was pretty upset with myself, falling over so early in this attempt at a game. But I think I have
come up with a solution!

Do attacking differently.

## New Attacking Idea
Before, I was attempting to have total freedom for attacking direction, which necessitated doing the
animations programmatically. But actually thinking about, this is an unnecessary shackle around my neck.

What I wanted, was for players to be able to choose their direction and angle of attack, rather than
having a predetermined pattern built in. So I thought about using movement to do that. But nothing
about this needs infinite degrees of freedom, and most likely will actually benefit for having a 
more restricted moveset.

So I'm going to restrict the attack choices to the 4 cardinal directions, their in-betweens, and maybe
a jump attack. That will give me 8 ~ 10 different attacks, and not only that, but I don't have to have
them be all simple slashes. 

I could have the forward movement attacks be thrusts, sideways slashes, and backwards swings more like
parries. I could put in extra code to incentivise alternating between left and right slashes. I have
a lot of options here, and I'm exciting to open up Godot again to have a go.

## Other projects
I've started moving some of my public repositories to [Codeberg](https://codeberg.org/Schwenckenator),
so you'll be able to find my dot-files there. I'm also planning on making a simple neovim plugin or two,
nothing too fancy though. 

I just want to find the fun in programming again, and I think I'll be okay if I keep searching for the fun.

I am having trouble sticking with it, with all that life throws at me, but I honesty have so much fun
when I'm doing game dev, and other programming projects, that I'll just have to remember that, and 
keep coming back.
