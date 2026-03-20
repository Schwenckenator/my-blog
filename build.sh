#!/usr/bin/env bash

# install packages
pip3 install commonmark
pip3 install python-frontmatter
pip3 install pygments

# run python script
python3 src/build_blog.py
