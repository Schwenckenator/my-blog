#!/usr/bin/env python3
import pprint as pp
import os
import glob
import commonmark
import frontmatter
import datetime
from zoneinfo import ZoneInfo
import re
import html as HTML

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class PageData:
    """A data class to hold page data"""

    def __init__(self, filepath, metadata, content):
        self.filepath = filepath
        self.metadata = metadata
        self.content = content


class CodeFormatter(HtmlFormatter):
    def wrap(self, source):
        return self._wrap_code(source)

    def _wrap_code(self, source):
        # print('wrapping code')
        # Open code tag
        yield 0, "<pre><code>"
        # Give all tokens
        for i, t in source:
            # print(i, t)
            yield i, t
        # Close code tag
        yield 0, "</code></pre>"
        # print('end wrapping code\n')


def get_key_regex(key):
    """Returns regex that will match a key"""
    return rf"{{{{\s*{key}\s*}}}}\n*"


def get_block_regex(key):
    """Returns regex that will match the block, and capture the contents"""
    return rf"{{{{\s*{key}\s*}}}}(.*?){{{{\s*/{key[1:]}\s*}}}}"


def fill_template(data_dict, template, date_format="%d %B %Y"):
    print("Filling template")
    keys = re.findall(r"{{\s*(.*?)\s*}}", template)
    result = template
    for key in keys:
        if key == "content":
            # Content is special, and will be replaced later
            continue

        if "#if" in key:
            result = fill_if(key, data_dict, result)
            continue

        if "#each" in key:
            result = fill_each(key, data_dict, result, date_format)
            continue

        result = fill_data(key, data_dict, result, date_format)

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
            pattern=regex, repl=get_match, string=template, count=1, flags=re.S
        )
    else:
        result = re.sub(pattern=regex, repl="", string=template, count=1, flags=re.S)
    return result


def fill_each(key, data_dict, template, date_format="%d %B %Y"):
    """Fill out the each block"""
    dict_key = key.replace("#each ", "")
    value = data_dict.get(dict_key)

    regex = get_block_regex(key)

    # If the value is not a list, something is wrong, just delete everything
    if not isinstance(value, list):
        result = re.sub(pattern=regex, repl="", string=template, count=1, flags=re.S)
        return result

    # Get the contents of the each block, to use as a template
    inner_template = re.search(regex, template, flags=re.S).group(1)

    content = ""

    # Loop through values of the list
    for v in value:
        # If not a dict, make it a dict with a dot for a key
        if not isinstance(v, dict):
            v = {".": v}

        # Fill the inner template out with the dictionary
        content += fill_template(v, inner_template, date_format) + "\n"

    # Replace each block with rendered content
    result = re.sub(
        pattern=regex,
        repl=content.replace("\\", "\\\\"),
        string=template,
        count=1,
        flags=re.S,
    )

    return result


def fill_data(key, data_dict, template, date_format="%d %B %Y"):
    value = data_dict.get(key)

    if value is None or isinstance(value, bool) or isinstance(value, list):
        return re.sub(
            pattern=rf"{{{{\s*{key}\s*}}}}",
            repl="",
            string=template,
            count=1,
        )

    if isinstance(value, datetime.date):
        dt = datetime.datetime(
            value.year, value.month, value.day, 0, 0, 0, tzinfo=ZoneInfo("Asia/Tokyo")
        )
        value = dt.strftime(date_format)
    return re.sub(
        pattern=rf"{{{{\s*{key}\s*}}}}",
        repl=str(value).replace("\\", "\\\\"),
        string=template,
        count=1,
    )


def load_file(path):
    print(f"Loading '{path}'")
    dir = path.rsplit("/", 1)[0]
    # Open file
    with open(path, "r") as file:
        is_markdown = path.rsplit(".", 1)[1] == "md"

        if is_markdown:
            # extract frontmatter and raw markdown
            metadata, raw = frontmatter.parse(file.read())

            # add `/img/` to image urls
            raw = re.sub(r"!\[(.*)\]\((.*)\)", r"![\1](/img/\2)", raw)

            # convert content to html
            content = commonmark.commonmark(raw)

            # Convert code blocks using pygments
            code_regex = r'<pre><code class="language-(.*?)">(.*?)<\/code><\/pre>'
            code_blocks = re.findall(code_regex, content, flags=re.S)

            print("\n\nChecking file - ", metadata["title"])

            for cb in code_blocks:
                try:
                    lexer = get_lexer_by_name(cb[0])
                    code = HTML.unescape(cb[1])
                    result = highlight(code, lexer, CodeFormatter())

                    content = re.sub(
                        pattern=code_regex,
                        repl=result.replace("\\", "\\\\"),
                        string=content,
                        count=1,
                        flags=re.S,
                    )

                except ClassNotFound:
                    continue

            # if the page is not published, don't include it in the build
            if not metadata["is_published"]:
                return
        else:
            content = file.read()
            metadata = {}

        # Save data in class
        page_data = PageData(path, metadata, content)
        # Append to list
        site_data[dir].append(page_data)


def render_file(path, dir):
    print(f"{path} is text!")

    # Get page data
    page = None
    for p in site_data[dir]:
        if p.filepath == path:
            page = p
            break

    if not page:
        print("ERROR: Page data is None")
        return

    template_paths = find_templates(dir)
    html = "{{ content }}"  # Seed for replacer
    content = page.content

    # Iteratively apply templates from root -> branch
    content_regex = get_key_regex("content")
    for t_path in template_paths:
        template = templates[t_path]

        # Fill keys
        html = fill_template(site_data, html)

        # Replace content
        html = re.sub(pattern=content_regex, repl=template, string=html)

    # Add page content to html
    # Fill keys
    html = fill_template(site_data, html)

    # Replace content
    print(html)
    html = re.sub(pattern=content_regex, repl=content, string=html)

    # destination = path.replace(source_dir, build_dir)
    slug = (
        page.metadata.get("slug")
        or os.path.splitext(os.path.basename(page.filepath))[0]
    )

    destination = os.path.join(build_dir, slug + ".html")

    with open(destination, "w") as file:
        file.write(html)


def handle_other_file(path):
    new_path = path.replace(source_dir, build_dir, 1)
    print(f"Copying file '{path}' to '{new_path}'")

    # Copy file directly to new directory
    copy_command = f'cp "{path}" "{new_path}"'
    os.system(copy_command)


def find_templates(dir):
    template_paths = []
    d = dir
    while d:
        if html_template_name in filetree[d]:
            template_paths.append(d + "/" + html_template_name)
        if "/" not in d:
            break
        # Remove the last slash and keep the rest
        d = d.rsplit("/", 1)[0]

    # Go from root -> branch
    template_paths.reverse()
    print("Found templates: ", template_paths)

    return template_paths


def decorate_code_blocks(content):
    # Convert code blocks using pygments
    code_regex = r'<pre><code class="language-(.*?)">(.*?)<\/code><\/pre>'
    code_blocks = re.findall(code_regex, content, flags=re.S)

    for cb in code_blocks:
        try:
            lexer = get_lexer_by_name(cb[0])
            code = HTML.unescape(cb[1])
            result = highlight(code, lexer, CodeFormatter())

            content = re.sub(
                pattern=code_regex,
                repl=result.replace("\\", "\\\\"),
                string=content,
                count=1,
                flags=re.S,
            )

        except ClassNotFound:
            continue

    return content


#######
# Main
#######

source_dir = "site"
build_dir = "dist"

html_template_name = "template.html"
rss_template = "rss-template.xml"
template_filenames = [html_template_name, rss_template]

# Dictionary<path -> template contents>
templates = {}

site_data = {}

# Delete current build folder
os.system("rm -rf dist")

# Dictionary<Directory -> filepath array>
filetree = {}

# Walk the directories
for root, dirs, files in os.walk(source_dir):
    filetree[root] = []
    site_data[root] = []

    for name in files:
        filetree[root].append(name)
        path = f"{root}/{name}"
        ext = name.rsplit(".", 1)[1]
        if name == html_template_name:
            # Load template
            with open(path, "r") as file:
                templates[path] = file.read()
        elif ext == "md" or ext == "html":
            load_file(path)

print(templates.keys())

print("Filetree")
# pp.pprint(filetree)
# pp.pprint(site_data)

for key in site_data:
    for page in site_data[key]:
        print(f"Page: '{page.filepath}', '{page.metadata.get("title")}'")

# Walk through the listed files

for dir in filetree:
    print(f"Checking dir '{dir}'")

    # Create directory in build folder
    new_dir = dir.replace(source_dir, build_dir, 1)
    os.mkdir(new_dir)
    print(f"Created directory '{new_dir}'")

    for filename in filetree[dir]:
        # Abort if this is a template file
        if filename in template_filenames:
            print(f"'{filename}' is a template filename, skipping...")
            continue

        name = dir + "/" + filename
        print(f"Checking file '{name}'")
        extension = filename.rsplit(".", 1)[1]
        match (extension):
            case "md" | "html":
                render_file(name, dir)
            case _:
                handle_other_file(name)


exit(0)


# A list of pages to save for the index page
pages = []

for f in glob.iglob(f"{source_dir}/**/*.md"):
    # Open markdown file
    with open(f, "r") as file:
        # extract frontmatter and raw markdown
        metadata, raw = frontmatter.parse(file.read())

        # add `/img/` to image urls
        raw = re.sub(r"!\[(.*)\]\((.*)\)", r"![\1](/img/\2)", raw)

        # convert content to html
        content = commonmark.commonmark(raw)

        # Convert code blocks using pygments
        code_regex = r'<pre><code class="language-(.*?)">(.*?)<\/code><\/pre>'
        code_blocks = re.findall(code_regex, content, flags=re.S)

        print("\n\nChecking file - ", metadata["title"])

        for cb in code_blocks:
            try:
                lexer = get_lexer_by_name(cb[0])
                code = HTML.unescape(cb[1])
                result = highlight(code, lexer, CodeFormatter())

                content = re.sub(
                    pattern=code_regex,
                    repl=result.replace("\\", "\\\\"),
                    string=content,
                    count=1,
                    flags=re.S,
                )

            except ClassNotFound:
                continue

    # if the page is not published, don't include it in the build
    if not metadata["is_published"]:
        continue

    # Save data in class
    page_data = PageData(f, metadata, content)
    # Append to pages list
    pages.append(page_data)

# Sort the pages by `publish_date`
pages.sort(key=lambda p: p.metadata["publish_date"], reverse=True)

for index, page in enumerate(pages):
    # Create pathname for build dir
    slug = page.metadata["slug"] or os.path.splitext(os.path.basename(page.filepath))[0]

    destination = os.path.join(build_dir, slug + ".html")

    # copy template to new variable
    html = templates["page"]

    # Prepare other article links
    if index > 0:
        next = pages[index - 1]
        page.metadata["next_href"] = str(next.metadata["slug"])
        page.metadata["next_title"] = str(next.metadata["title"])

    if index < len(pages) - 1:
        prev = pages[index + 1]
        page.metadata["prev_href"] = prev.metadata["slug"]
        page.metadata["prev_title"] = prev.metadata["title"]

    html = fill_template(page.metadata, html)

    # replace the content template handle with the content from the html
    html = html.replace("{{ content }}", page.content)

    with open(destination, "w") as file:
        # write file
        file.write(html)

    print(f"file written to {destination}")


# Create index page
html = templates["index"]
destination = os.path.join(build_dir, "index.html")
content = ""

index_data = {"pages": []}
for page in pages:
    index_data["pages"].append(page.metadata)

html = fill_template(index_data, templates["index"])

with open(destination, "w") as file:
    file.write(html)

print("index page finished")

# Create RSS file
rss = templates["rss-feed"]
destination = os.path.join(build_dir, "rss.xml")
rss_date_format = "%a, %d %b %Y %H:%M:%S %z"
rss_data = {
    "build_date": datetime.datetime.now(tz=ZoneInfo("Asia/Tokyo")).strftime(
        rss_date_format
    ),
    "items": [],
}

for page in pages:
    data = page.metadata
    data["article"] = HTML.escape(page.content)
    rss_data["items"].append(data)


rss = fill_template(rss_data, templates["rss-feed"], rss_date_format)

with open(destination, "w") as file:
    file.write(rss)

print("finished building rss feed")

print("finished successfully!")
