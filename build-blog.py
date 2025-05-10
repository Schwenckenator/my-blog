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


def get_block_regex(key):
    """Returns regex that will match the block, and capture the contents"""
    return fr"{{{{\s*{key}\s*}}}}(.*?){{{{\s*/{key[1:]}\s*}}}}"


def fill_template(data_dict, template):
    keys = re.findall(r"{{\s*(.*?)\s*}}", template)
    result = template
    for key in keys:

        if '#if' in key:
            result = fill_if(key, data_dict, result)
            continue

        if '#each' in key:
            result = fill_each(key, data_dict, result)
            continue

        result = fill_data(key, data_dict, result)

    return result


def get_match(match):
    if match.group(1):
        return match.group(1)
    return ""


def fill_if(key, data_dict, template):

    result = template
    condition = key.replace("#if ", "")
    value = data_dict.get(condition)

    regex = get_block_regex(key)

    if value:
        result = re.sub(
            pattern=regex,
            repl=get_match,
            string=template,
            count=1,
            flags=re.S
        )
    else:
        result = re.sub(
            pattern=regex,
            repl="",
            string=template,
            count=1,
            flags=re.S
        )
    return result


def fill_each(key, data_dict, template):
    dict_key = key.replace("#each ", "")
    value = data_dict.get(dict_key)

    regex = get_block_regex(key)

    if not isinstance(value, list):
        result = re.sub(
            pattern=regex,
            repl="",
            string=template,
            count=1,
            flags=re.S
        )
        return result

    inner_template = re.search(regex, template, flags=re.S).group(1)

    content = ""

    for v in value:
        print('v', v)
        # If not a dict, make it a dict with a dot for a key
        if not isinstance(v, dict):
            v = {'.': v}

        content += fill_template(v, inner_template) + "\n"

    result = re.sub(
        pattern=regex,
        repl=content,
        string=template,
        count=1,
        flags=re.S
    )

    return result


def fill_data(key, data_dict, template):
    value = data_dict.get(key)

    if value is None or isinstance(value, bool) or isinstance(value, list):
        return re.sub(
            pattern=fr"{{{{\s*{key}\s*}}}}",
            repl="",
            string=template,
            count=1,
        )

    if isinstance(value, datetime.date):
        value = value.strftime("%d %B %Y")

    return re.sub(
        pattern=fr"{{{{\s*{key}\s*}}}}",
        repl=str(value),
        string=template,
        count=1,
    )


def template_replace(metadata, template):
    """replaces the template placeholder with metadata"""
    result = template
    for key, value in metadata.items():
        # print('metadata key - ', key, '; value - ', value)
        if value is None:
            # print("It's NONE, deleting the handler")
            result = result.replace(f"{{{{ {key} }}}}", "")
            continue
        if isinstance(value, list):
            # print("It's a list, do nothing")
            result = replace_template_each(key, value, result)
            continue
        if isinstance(value, bool):
            # print("It's a bool, don't replace anything!", value)
            continue
        if isinstance(value, datetime.date):
            # print("It's a date!", value)
            value = value.strftime("%d %B %Y")
        # print('final value', value)
        result = result.replace(f"{{{{ {key} }}}}", value)
    return result


def replace_template_each(each_key, data_list, template):
    """replaces a list block"""
    print('replace_template_each')

    print('each_key', each_key)
    # print('data_list', data_list)
    # print('template', template)

    each_start = f"{{{{ #each {each_key} }}}}"
    each_end = f"{{{{ /each {each_key} }}}}"
    regex = fr"{each_start}(.*?){each_end}"
    print('each_start', each_start)
    print('each_end', each_end)
    print('regex', regex)

    matches = re.search(regex, template, re.S)
    each_block = ""

    print('matches', matches)

    if matches:
        each_block = matches.group(1)
    else:
        return template

    content = ""
    result = template

    for data in data_list:
        print('data', data)
        item = each_block
        if isinstance(data, dict):
            print('data is dict', data)
            item = template_replace(data, item)
            print('item', item)
        else:
            print('data is NOT dict', data)
            item = template_replace({'.': data}, item)
            print('item', item)
        content += item + "\n"

    print('content', content)
    result = re.sub(regex, content, template, flags=re.S)
    print('each result', result)

    return result


#######
# Main
#######

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
    # html = fill_template(page.metadata, html)

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

index_data = {'pages': []}
for page in pages:
    index_data['pages'].append(page.metadata)

html = fill_template(index_data, template['index'])
print(html)

with open(destination, 'w') as file:
    file.write(html)

print("finished successfully!")
