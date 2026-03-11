---
title: Starting a new prototype
publish_date: 2026-01-25
is_published: true
slug: new-game-prototype
description: True to my word, I have started work on a new game!
tags:
  - game-dev
  - personal
---

True to my work, I have started work on a new game!

## My week of dev
So this blog is a little bit later than what I wanted, but sometimes life happens, and you sort
out the fun stuff later. 

I started work on my new game on Last Friday, firing up my Godot Editor, and added some simple multiplayer.
I say 'added' like it was easy, but it took a little bit of wrangling to fix my own shortcuts that 
exploded the engine. 

> It turns out, if you follow the documentation properly, it works.

But all in all, valuable learning experience. Especially where you can, and cannot, take shortcuts.
By Tuesday, I had local multiplayer connections working, and I could see my character move around.

Then I began work on the actual meat of the game. I want to have a melee system with fine control
over the angle of attack. To begin with, I thought of using actual physics objects for the sword,
so it could bounce off armour using the physics system. I then proceeded to lose half a night wondering
why the 6DOF spring joint wasn't working no matter how high I cranked the numbers.

> It turns out, GodotPhysics has not implemented springs in their joints.

A quick switch to JoltPhysics, and my sword sprang to life! \
But it was not meant to be. 

Using physics joints for swords, means I needed to have another physics object for the hand. 
And once I started moving these around, the sword was getting stuck in the floor, dragging around, 
I could never get it to stay straight, etc etc etc.

I could tell pretty quick that this was probably a dead end. So I'll have to code the movement manually.

And on Tuesday, I got the first step of my attack done.

### Attacking
So the way it works, is when the attack is held, movement translates to hand position. Moving left,
moves your hand left, which will make a left to right slice. The idea is, by mixing horizontal and vertical
movement, you could change the angle of attack to precisely avoid armour. 

I got the first step, moving the hands based on your movement, finished.

Then I crashed. For the rest of the week.

## Why?
Well, full time work + parenting + hobby is hard work, and I probably pushed myself a little too hard,
too fast. This prototype, and the game I hope to make out of it, is a marathon, and not a sprint.
So I'll need to find a rhythm that works for me. And I'll use this blog to keep my honest.

But, it's a new week now, so I'll be back at it on Monday, and I'll have the next write-up done on 
Friday!

See you then!
