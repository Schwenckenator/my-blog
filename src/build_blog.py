#!/usr/bin/env python3
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


def get_block_regex(key):
    """Returns regex that will match the block, and capture the contents"""
    return rf"{{{{\s*{key}\s*}}}}\n*(.*?){{{{\s*/{key[1:]}\s*}}}}\n*"


def fill_template(data_dict, template, date_format="%d %B %Y"):
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
            pattern=rf"{{{{\s*{key}\s*}}}}\n*",
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
        pattern=rf"{{{{\s*{key}\s*}}}}\n*",
        repl=str(value).replace("\\", "\\\\"),
        string=template,
        count=1,
    )


#######
# Main
#######
def main():
    source_dir = "site"
    build_dir = "dist"

    # Delete current build folder
    os.system(f"rm -rf {build_dir}")
    # Make a new one
    os.mkdir(build_dir)
    os.mkdir(f"{build_dir}/blog")

    # copy css and img directories to build
    copy_dirs = ["css", "img", "js"]
    for dir in copy_dirs:
        copy_command = f'cp -r "./{source_dir}/{dir}" "./{build_dir}/{dir}"'
        os.system(copy_command)

    templates = {}

    for path in glob.iglob(f"{source_dir}/**/template.html", recursive=True):
        dir = path.rsplit("/", 1)[0]
        print("path", path, dir)
        with open(path) as file:
            templates[dir] = file.read()

    # Load rss template
    with open(f"{source_dir}/rss-template.xml") as file:
        templates["rss-feed"] = file.read()

    # for key in templates:
    #     print(templates[key])

    # A list of pages to save for the index page
    blogs = []

    for path in glob.iglob(f"{source_dir}/**/*.md"):
        # Open markdown file
        with open(path, "r") as file:
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
        page_data = PageData(path, metadata, content)
        # Append to pages list
        blogs.append(page_data)

    # Sort the pages by `publish_date`
    blogs.sort(key=lambda p: p.metadata["publish_date"], reverse=True)

    for index, page in enumerate(blogs):
        # Create pathname for build dir
        slug = (
            page.metadata["slug"]
            or os.path.splitext(os.path.basename(page.filepath))[0]
        )

        destination = os.path.join(build_dir, "blog", slug + ".html")

        # copy template to new variable
        html = templates["site"]
        # Apply blog template to base template
        html = html.replace("{{ content }}\n", templates["site/blog"])

        # Prepare other article links
        if index > 0:
            next = blogs[index - 1]
            page.metadata["next_href"] = str(next.metadata["slug"])
            page.metadata["next_title"] = str(next.metadata["title"])

        if index < len(blogs) - 1:
            prev = blogs[index + 1]
            page.metadata["prev_href"] = prev.metadata["slug"]
            page.metadata["prev_title"] = prev.metadata["title"]

        html = fill_template(page.metadata, html)

        # replace the content template handle with the content from the html
        html = html.replace("{{ content }}\n", page.content)

        with open(destination, "w") as file:
            # write file
            file.write(html)

        print(f"file written to {destination}")

    index_data = {"blog": [], "latest_blog": []}
    for page in blogs:
        index_data["blog"].append(page.metadata)

    # Only show latest 5
    for page in blogs[:5]:
        index_data["latest_blog"].append(page.metadata)

    # Create html pages
    for path in glob.iglob(f"{source_dir}/**/*.html", recursive=True):
        if "template.html" in path:
            continue

        # Create index page
        html = templates["site"]
        destination = path.replace(source_dir, build_dir)
        content = ""

        with open(path, "r") as file:
            content = file.read()

        # Fill out base template with page content
        html = html.replace("{{ content }}\n", content)
        html = fill_template(index_data, html)

        with open(destination, "w") as file:
            file.write(html)

        print(f"'{path}' page finished")

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

    for page in blogs:
        data = page.metadata
        data["article"] = HTML.escape(page.content)
        rss_data["items"].append(data)

    rss = fill_template(rss_data, templates["rss-feed"], rss_date_format)

    with open(destination, "w") as file:
        file.write(rss)

    print("finished building rss feed")

    print("finished successfully!")


# Run if main
if __name__ == "__main__":
    main()
