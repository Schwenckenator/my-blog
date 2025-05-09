#!/usr/bin/env python3
import os
import glob
import commonmark
import frontmatter
import datetime
import re


class PageData():
    """A data class to hold page data"""

    def __init__(self, filepath, metadata, content):
        self.filepath = filepath
        self.metadata = metadata
        self.content = content


def template_replace(metadata, template):
    """replaces the template placeholder with metadata"""
    result = template
    for key, value in metadata.items():
        print('metadata key - ', key, '; value - ', value)
        if value is None:
            print("It's NONE, deleting the handler")
            result = result.replace(f"{{{{ {key} }}}}", "")
            continue
        if isinstance(value, list):
            print("It's a list, do nothing")
            continue
        if isinstance(value, bool):
            print("It's a bool, don't replace anything!", value)
            continue
        if isinstance(value, datetime.date):
            print("It's a date!", value)
            value = value.strftime("%d %B %Y")
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
with open('./src/templates/next-link.partial.html', 'r') as file:
    template['next-link'] = file.read()
with open('./src/templates/prev-link.partial.html', 'r') as file:
    template['prev-link'] = file.read()
with open('./src/templates/tag.partial.html', 'r') as file:
    template['tag'] = file.read()

# A list of pages to save for the index page
pages = []

for f in glob.iglob(f"{source_dir}/**/*.md"):
    # Open markdown file
    with open(f, 'r') as file:
        # extract frontmatter and raw markdown
        metadata, raw = frontmatter.parse(file.read())

        # add `/img/` to image urls
        raw = re.sub(r"!\[(.*)\]\((.*)\)", r"![\1](/img/\2)", raw)

        # convert content to html
        content = commonmark.commonmark(raw)

    # if the page is not published, don't include it in the build
    if not metadata['is_published']:
        continue

    # Save data in class
    page_data = PageData(f, metadata, content)
    # Append to pages list
    pages.append(page_data)

# Sort the pages by `publish_date`
pages.sort(key=lambda p: p.metadata['publish_date'], reverse=True)

for index, page in enumerate(pages):
    # Create pathname for build dir
    slug = page.metadata['slug'] or os.path.splitext(
        os.path.basename(page.filepath))[0]

    destination = os.path.join(build_dir, slug + '.html')

    # copy template to new variable
    html = template['page']

    # Prepare other article links
    if index > 0:
        next = pages[index-1]
        link_metadata = {
            'href': next.metadata['slug'],
            'title': next.metadata['title'],
        }
        link = template_replace(link_metadata, template['next-link'])
        page.metadata['next_link'] = link
    else:
        # Delete the template handle
        page.metadata['next_link'] = None

    if index < len(pages) - 1:
        prev = pages[index+1]
        link_metadata = {
            'href': prev.metadata['slug'],
            'title': prev.metadata['title'],
        }
        link = template_replace(link_metadata, template['prev-link'])
        page.metadata['prev_link'] = link
    else:
        # Delete the template handle
        page.metadata['prev_link'] = None

    # replace the other handles
    html = template_replace(page.metadata, html)

    # replace the content template handle with the content from the html
    html = html.replace("{{ content }}", page.content)

    with open(destination, 'w') as file:
        # write file
        file.write(html)

    print(f"file written to {destination}")


# Create index page
html = template['index']
destination = os.path.join(build_dir, 'index.html')
content = ""

for page in pages:
    print('page metadata - ', page.metadata)

    tags_html = ""
    if page.metadata.get('tags'):
        for tag in page.metadata['tags']:
            tag_template = template['tag']
            tag_html = tag_template.replace("{{ tag }}", tag)
            tags_html += tag_html + "\n"

    page.metadata['tag_list'] = tags_html

    # Replace metadata handles
    link_html = template_replace(page.metadata, template['page-link'])
    # Add new link to index content
    content += link_html + "\n"

html = html.replace("{{ content }}", content)
with open(destination, 'w') as file:
    file.write(html)

print("finished successfully!")
