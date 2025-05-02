#!/usr/bin/env python3
import os
import glob
import commonmark
import frontmatter

source_dir = "src"
build_dir = "build"

# Delete current build folder
os.system('rm -rf build')
# Make a new one
os.mkdir(build_dir)

# copy css and img directories to build
copy_dirs = ["css", "img"]
for dir in copy_dirs:
    copy_command = f"cp -r \"./{source_dir}/{dir}\" \"./{build_dir}/{dir}\""
    os.system(copy_command)

template = {}
# Read template
with open('./src/templates/index-template.html', 'r') as file:
    template['index'] = file.read()
with open('./src/templates/page-template.html', 'r') as file:
    template['page'] = file.read()

# Loop over glob of markdown files in 'pages' directory
for f in glob.iglob(f"{source_dir}/**/*.md"):
    # Open markdown file
    with open(f, 'r') as file:
        metadata, raw = frontmatter.parse(file.read())
        # raw = file.read()
        # convert content to html
        content = commonmark.commonmark(raw)

    print('metadata', metadata)

    # Create pathname for build dir
    # NOTE: Does this work like javascript?
    slug = metadata['slug'] or os.path.splitext(os.path.basename(f))[0]

    destination = os.path.join(build_dir, slug + '.html')

    # copy template to new variable
    html = template['page']
    # replace the content template handle with the content from the html
    html = html.replace("{{ content }}", content)

    for key, value in metadata.items():
        print('metadata key - ', key)
        print('metadata value - ', value)
        html = html.replace(f"{{{{ {key} }}}}", str(value))

    with open(destination, 'w') as file:
        # write file
        file.write(html)

    print(f"file written to {destination}")

print("finished successfully!")
