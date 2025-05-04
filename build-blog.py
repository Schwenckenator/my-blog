#!/usr/bin/env python3
import os
import glob
import commonmark
import frontmatter
import datetime


def template_replace(metadata, template):
    result = template
    for key, value in metadata.items():
        print('metadata key - ', key, '; value - ', value)
        if isinstance(value, bool):
            print("It's a bool, don't replace anything!", value)
            continue
        if isinstance(value, datetime.date):
            print("It's a date!", value)
            value = value.strftime("%d %B %Y")
        else:
            print("It's not a date.", value)
        print('final value', value)
        result = result.replace(f"{{{{ {key} }}}}", value)
    return result


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
with open('./src/templates/page-link.partial.html', 'r') as file:
    template['page-link'] = file.read()

# A list of pages to save for the index page
pages = []

# Loop over glob of markdown files in 'pages' directory
for f in glob.iglob(f"{source_dir}/**/*.md"):
    # Open markdown file
    with open(f, 'r') as file:
        # extract frontmatter and raw markdown
        metadata, raw = frontmatter.parse(file.read())
        # convert content to html
        content = commonmark.commonmark(raw)

    # if the page is not published, don't include it in the build
    if not metadata['is_published']:
        continue

    # Save metadata for index page later
    pages.append(metadata)

    print('metadata', metadata)

    # Create pathname for build dir
    slug = metadata['slug'] or os.path.splitext(os.path.basename(f))[0]

    destination = os.path.join(build_dir, slug + '.html')

    # copy template to new variable
    html = template['page']
    # replace the content template handle with the content from the html
    html = html.replace("{{ content }}", content)

    # replace the other handles
    html = template_replace(metadata, html)

    with open(destination, 'w') as file:
        # write file
        file.write(html)

    print(f"file written to {destination}")

# Create index page
html = template['index']
destination = os.path.join(build_dir, 'index.html')
content = ""

for page in pages:
    print('page - ', page)
    # Replace metadata handles
    link_html = template_replace(page, template['page-link'])
    # Add new link to index content
    content += link_html + "\n"

html = html.replace("{{ content }}", content)
with open(destination, 'w') as file:
    file.write(html)

print("finished successfully!")
