#include <dirent.h>
#include <errno.h>
#include <linux/limits.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <unistd.h>
#include <yaml.h>

typedef struct {
    char *content;
    char *title;
    char *publish_date;
    char *is_published;
    char *slug;
    char *description;
    char *tags[];
} BlogPage;

typedef struct {
    char *content;
    char *slug;
} Page;

// #!/usr/bin/env python3
// import os
// import glob
// import commonmark
// import frontmatter
// import datetime
// from zoneinfo import ZoneInfo
// import re
// import html as HTML
//
// from pygments import highlight
// from pygments.lexers import get_lexer_by_name
// from pygments.formatters import HtmlFormatter
// from pygments.util import ClassNotFound

/** Gets the size in bytes */
static size_t get_file_size(const char *filename);

/** Read the full contents of a file into a buffer and return it */
static char *read_file(const char *filename);
static int walk_directory(const char *dirname);
static bool read_pagedata(const char *filepath, BlogPage *page);
static bool extract_blogpage_metadata(char *contents, BlogPage *page);
static int render_markdown();

// TODO
// - Walk the directories, gathering information about the templates, pages, and
// markdown files
// - Walk the information, building each page and saving to dist folder
// - Build a `tree` to hold the info?

// I need:
// - A list of blog pages, struct BlogPage
//

// TODO: Make this extendable
BlogPage blog_pages[16];
int blog_page_count = 0;

/*
 * NOTE: argc is ARG_COUNT
 * argv[] is ARG_VALUES
 */
int main(int argc, char *argv[]) {
    // ******
    // * Main
    // ******
    char cwd[PATH_MAX];
    getcwd(cwd, sizeof(cwd));
    printf("Current cwd: '%s'\n", cwd);

    char site_dir[] = "site";
    char export_dir[] = "dist";

    printf("Deleting 'dist'\n");

    // Delete current build folder
    // NOTE: I tried using 'unlink' and 'rmdir' but just using the shell is
    // easier
    system("rm -rf dist");

    // Make a new one, with read write permissions
    mkdir(export_dir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

    // Walk directories from current
    printf("### Walking directories");
    walk_directory("./site");

    printf("Printing found blog pages");
    for (int i = 0; i < blog_page_count; i++) {
        printf("%s\n", blog_pages[i].title);
    }

    // Begin walk of 'site' directory

    // Pointer for directory entry
    // struct dirent *de;
    //
    // DIR *dr = opendir(".");
    //
    // if (dr == NULL) {
    //     printf("Could not open directory\n");
    //     return 0;
    // }
    //
    // while ((de = readdir(dr)) != NULL) {
    //     switch (de->d_type) {
    //     case DT_REG:
    //         printf("%s\n", de->d_name);
    //         break;
    //     case DT_DIR:
    //         printf("%s/\n", de->d_name);
    //         break;
    //     case DT_LNK:
    //         printf("%s@\n", de->d_name);
    //         break;
    //     default:
    //         printf("%s*\n", de->d_name);
    //     }
    // }
    //
    // closedir(dr);
    return 0;

    //
    // for f in glob.iglob(f"{source_dir}/**/*.md"):
    //     # Open markdown file
    //     with open(f, 'r') as file:
    //         # extract frontmatter and raw markdown
    //         metadata, raw = frontmatter.parse(file.read())
    //
    //        # add `/img/` to image urls
    //        raw = re.sub(r"!\[(.*)\]\((.*)\)", r"![\1](/img/\2)", raw)
    //
    //        # convert content to html
    //        content = commonmark.commonmark(raw)
    //
    //        # Convert code blocks using pygments
    //        code_regex = r'<pre><code
    //        class="language-(.*?)">(.*?)<\/code><\/pre>' code_blocks =
    //        re.findall(code_regex, content, flags=re.S)
    //
    //        print('\n\nChecking file - ', metadata['title'])
    //
    //        for cb in code_blocks:
    //            try:
    //                lexer = get_lexer_by_name(cb[0])
    //                code = HTML.unescape(cb[1])
    //                result = highlight(code, lexer, CodeFormatter())
    //
    //                content = re.sub(
    //                    pattern=code_regex,
    //                    repl=result.replace("\\", "\\\\"),
    //                    string=content,
    //                    count=1,
    //                    flags=re.S
    //                )
    //
    //            except ClassNotFound:
    //                continue
    //
    //    # if the page is not published, don't include it in the build
    //    if not metadata['is_published']:
    //        continue
    //
    //    # Save data in class
    //    page_data = PageData(f, metadata, content)
    //    # Append to pages list
    //    pages.append(page_data)
    //
    // # Sort the pages by `publish_date`
    // pages.sort(key=lambda p: p.metadata['publish_date'], reverse=True)
    //
    // for index, page in enumerate(pages):
    //     # Create pathname for build dir
    //     slug = page.metadata['slug'] or os.path.splitext(
    //         os.path.basename(page.filepath))[0]
    //
    //    destination = os.path.join(build_dir, slug + '.html')
    //
    //    # copy template to new variable
    //    html = template['page']
    //
    //    # Prepare other article links
    //    if index > 0:
    //        next = pages[index-1]
    //        page.metadata['next_href'] = str(next.metadata['slug'])
    //        page.metadata['next_title'] = str(next.metadata['title'])
    //
    //    if index < len(pages) - 1:
    //        prev = pages[index+1]
    //        page.metadata['prev_href'] = prev.metadata['slug']
    //        page.metadata['prev_title'] = prev.metadata['title']
    //
    //    html = fill_template(page.metadata, html)
    //
    //    # replace the content template handle with the content from the html
    //    html = html.replace("{{ content }}", page.content)
    //
    //    with open(destination, 'w') as file:
    //        # write file
    //        file.write(html)
    //
    //    print(f"file written to {destination}")
    //
    //
    // # Create index page
    // html = template['index']
    // destination = os.path.join(build_dir, 'index.html')
    // content = ""
    //
    // index_data = {'pages': []}
    // for page in pages:
    //     index_data['pages'].append(page.metadata)
    //
    // html = fill_template(index_data, template['index'])
    //
    // with open(destination, 'w') as file:
    //     file.write(html)
    //
    // print("index page finished")
    //
    // # Create RSS file
    // rss = template['rss-feed']
    // destination = os.path.join(build_dir, 'rss.xml')
    // rss_date_format = "%a, %d %b %Y %H:%M:%S %z"
    // rss_data = {
    //     'build_date':
    //     datetime.datetime.now(tz=ZoneInfo('Asia/Tokyo')).strftime(rss_date_format),
    //     'items': [],
    // }
    //
    // for page in pages:
    //     data = page.metadata
    //     data['article'] = HTML.escape(page.content)
    //     rss_data['items'].append(data)
    //
    //
    // rss = fill_template(rss_data, template['rss-feed'], rss_date_format)
    //
    // with open(destination, 'w') as file:
    //     file.write(rss)
    //
    // print("finished building rss feed")
    //
    // print("finished successfully!")
}
// class PageData():
//     """A data class to hold page data"""
//
//    def __init__(self, filepath, metadata, content):
//        self.filepath = filepath
//        self.metadata = metadata
//        self.content = content
//
//
// class CodeFormatter(HtmlFormatter):
//     def wrap(self, source):
//         return self._wrap_code(source)
//
//    def _wrap_code(self, source):
//        # print('wrapping code')
//        # Open code tag
//        yield 0, '<pre><code>'
//        # Give all tokens
//        for i, t in source:
//            # print(i, t)
//            yield i, t
//        # Close code tag
//        yield 0, '</code></pre>'
//        # print('end wrapping code\n')
//
//
// def get_block_regex(key):
//     """Returns regex that will match the block, and capture the
//     contents""" return
//     fr"{{{{\s*{key}\s*}}}}(.*?){{{{\s*/{key[1:]}\s*}}}}"
//
//
// def fill_template(data_dict, template, date_format="%d %B %Y"):
//     print('Filling template')
//     keys = re.findall(r"{{\s*(.*?)\s*}}", template)
//     result = template
//     for key in keys:
//         if key == 'content':
//             # Content is special, and will be replaced later
//             continue
//
//        if '#if' in key:
//            result = fill_if(key, data_dict, result)
//            continue
//
//        if '#each' in key:
//            result = fill_each(key, data_dict, result, date_format)
//            continue
//
//        result = fill_data(key, data_dict, result, date_format)
//
//    return result
//
//
// def get_match(match):
//     if match.group(1):
//         return match.group(1)
//     return ""
//
//
// def fill_if(key, data_dict, template):
//     result = template
//
//    condition = key.replace("#if ", "")
//    value = data_dict.get(condition)
//
//    regex = get_block_regex(key)
//
//    if value:
//        result = re.sub(
//            pattern=regex,
//            repl=get_match,
//            string=template,
//            count=1,
//            flags=re.S
//        )
//    else:
//        result = re.sub(
//            pattern=regex,
//            repl="",
//            string=template,
//            count=1,
//            flags=re.S
//        )
//    return result
//
//
// def fill_each(key, data_dict, template, date_format="%d %B %Y"):
//     """Fill out the each block"""
//     dict_key = key.replace("#each ", "")
//     value = data_dict.get(dict_key)
//
//    regex = get_block_regex(key)
//
//    # If the value is not a list, something is wrong, just delete
//    everything if not isinstance(value, list):
//        result = re.sub(
//            pattern=regex,
//            repl="",
//            string=template,
//            count=1,
//            flags=re.S
//        )
//        return result
//
//    # Get the contents of the each block, to use as a template
//    inner_template = re.search(regex, template, flags=re.S).group(1)
//
//    content = ""
//
//    # Loop through values of the list
//    for v in value:
//        # If not a dict, make it a dict with a dot for a key
//        if not isinstance(v, dict):
//            v = {'.': v}
//
//        # Fill the inner template out with the dictionary
//        content += fill_template(v, inner_template, date_format) + "\n"
//
//    # Replace each block with rendered content
//    result = re.sub(
//        pattern=regex,
//        repl=content.replace("\\", "\\\\"),
//        string=template,
//        count=1,
//        flags=re.S
//    )
//
//    return result
//
//
// def fill_data(key, data_dict, template, date_format="%d %B %Y"):
//     value = data_dict.get(key)
//
//    if value is None or isinstance(value, bool) or isinstance(value,
//    list):
//        return re.sub(
//            pattern=fr"{{{{\s*{key}\s*}}}}",
//            repl="",
//            string=template,
//            count=1,
//        )
//
//    if isinstance(value, datetime.date):
//        dt = datetime.datetime(value.year, value.month,
//                               value.day, 0, 0, 0,
//                               tzinfo=ZoneInfo('Asia/Tokyo'))
//        value = dt.strftime(date_format)
//    return re.sub(
//        pattern=fr"{{{{\s*{key}\s*}}}}",
//        repl=str(value).replace("\\", "\\\\"),
//        string=template,
//        count=1,
//    )
//

static int walk_directory(const char *dirname) {
    char buffer[PATH_MAX + 2];
    char *p = buffer;
    char *end = &buffer[PATH_MAX];

    printf("Walking Dir: '%s'\n", dirname);
    bool is_blog_dir = strcmp(dirname, "./site/blog") == 0;
    printf("Is blog dir? %b\n", is_blog_dir);

    // Copy directory name to buffer
    const char *src = dirname;
    // NOTE: Can't just `strcpy` the string, because the position of the
    // 'p' pointer is important later
    while (p < end && *src != '\0') {
        *p++ = *src++;
    }
    *p = '\0';

    // Open the directory
    DIR *dir = opendir(dirname);
    if (!dir) {
        // Could not open directory
        fprintf(stderr, "Cannot open %s (%s)\n", dirname, strerror(errno));

        // Return FAILURE
        return 0;
    }

    // Print all files and sub-directories within the directory
    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
        // Creating a new pointer starting at the 'p' pointer
        char *q = p;
        char c;

        // Get final character of directory name
        if (buffer < q) {
            c = q[-1];
        } else {
            c = ':';
        }

        // Append Directory separator if not already there
        if (c != ':' && c != '/' && c != '\\') {
            *q++ = '/';
        }

        // Append file name
        src = ent->d_name;
        while (q < end && *src != '\0') {
            *q++ = *src++;
        }
        *q = '\0';

        switch (ent->d_type) {
        case DT_REG:
        case DT_LNK:
            printf("%s\n", buffer);
            if (is_blog_dir) {
                // Is markdown file?
                // Read through all characters of the buffer, check if the last
                // three are `.md`
                int len = strlen(buffer);
                if (len > 3 &&                //
                    buffer[len - 3] == '.' && //
                    buffer[len - 2] == 'm' && //
                    buffer[len - 1] == 'd'    //
                ) {
                    read_pagedata(buffer, &blog_pages[blog_page_count]);
                    ++blog_page_count;
                }
            }
            break;
        case DT_DIR:
            if (strcmp(ent->d_name, ".") != 0 && strcmp(ent->d_name, "..")) {
                // printf("Walk Dir: %s\n", buffer);
                walk_directory(buffer);
            }
        }
    }

    closedir(dir);
    // SUCCESS
    return 1;
}

static bool read_pagedata(const char *filename, BlogPage *page) {
    printf("Reading file: %s\n", filename);
    char *contents = read_file(filename);

    printf("Extracting Frontmatter from: %s\n", filename);
    if (!extract_blogpage_metadata(contents, page)) {
        fprintf(stderr, "Failed to extract page frontmatter: %s\n",
                strerror(errno));
    }

    printf("Extracted Frontmatter\n");
    printf("\tTitle: %s\n", page->title);
    printf("\tDescription: %s\n", page->description);
    printf("\tIs Published: %s\n", page->is_published);
    printf("\tPublish Date: %s\n", page->publish_date);
    printf("\tSlug: %s\n", page->slug);
    // printf("\tTitle: %s", page->slug);

    // Copy title for now
    // char *title = malloc(sizeof(char) * strlen(filename));
    // strcpy(title, filename);
    // page->title = title;

    // Success!
    return true;
}

static size_t get_file_size(const char *filename) {
    struct stat sb;
    if (stat(filename, &sb) != 0) {
        fprintf(stderr, "'stat' failed for '%s': %s", filename,
                strerror(errno));
        exit(EXIT_FAILURE);
    }
    return sb.st_size;
}

static char *read_file(const char *filename) {
    size_t size = 0;
    char *contents;

    size = get_file_size(filename);
    contents = malloc(size + 1);

    if (!contents) {
        fprintf(stderr, "Not enough memory. Attempted to allocate %zu bytes.\n",
                size);
        return false;
    }

    FILE *file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Failed to open file '%s': %s\n", filename,
                strerror(errno));
        // FAILED
        return false;
    }

    size_t bytes_read = fread(contents, sizeof(char), size, file);
    if (bytes_read != size) {
        fprintf(stderr,
                "Short read of '%s': Expected %zu bytes but got %zu: %s\n",
                filename, size, bytes_read, strerror(errno));
        return false;
    }

    int status = fclose(file);
    if (status != 0) {
        fprintf(stderr, "Failed to close file '%s': %s\n", filename,
                strerror(errno));
        return false;
    }

    return contents;
}

static bool is_alpha(char c) {
    return (c >= 'a' && c <= 'z') || // format
           (c >= 'A' && c <= 'Z') || // blocking comment
           c == '_';
}

static bool extract_blogpage_metadata(char *contents, BlogPage *page) {
    // NOTE:
    // Frontmatter must be the first thing in the file
    // Frontmatter starts with three hyphens `---`
    // Frontmatter has `key: value` pairs
    // Frontmatter ends with three hyphens `---`
    // This parser will support bool, strings, and arrays of strings only

    // Prepare scanner to read content
    char *start = contents;
    char *current = contents;

    printf("Extracting Frontmatter\n");

    // Check if the frontmatter is at the start of the file
    // the first three characters need to be '---' with a newline
    bool in_frontmatter = true;
    for (int i = 0; i < 3; i++) {
        if (*current != '-') {
            in_frontmatter = false;
            break;
        }
        // Advance pointer
        current++;
    }
    // After three hyphens, we need a newline
    if (*current != '\n') {
        in_frontmatter = false;
    }

    if (!in_frontmatter) {
        printf("Frontmatter missing or malformed\n");
        // Frontmatter is missing or malformed, bail
        return false;
    }

    bool is_key = true;

    char key[4096];
    char value[4096];

    // Start reading the frontmatter
    printf("Reading Chars...\n");
    do {
        start = current;
        // Read key
        current++;
        char c = current[-1];
        printf("%c", c);

        switch (c) {
        case '-':
            if (*current == '-' && current[1] == '-') {
                in_frontmatter = false;
            } else {
                // An array value?
                if (*current == ' ')
                    // Skip space
                    current++;
            }
            break;
        case ':':
            // Split between key and value
            is_key = false;
            if (*current == ' ')
                current++;
            break;
        case '\n':
            is_key = true;
            break;
        default:
            // Turn whatever this is into a string
            if (is_key) {
                // Copy bytes into key variable until a ':' is hit
                while (*current != ':' && *current != '\n' &&
                       *current != '\0') {
                    printf("%c", *current);
                    current++;
                }
                strlcpy(key, start, (int)(current - start) + 1);
                printf("\nFOUND Key: '%s'\n", key);
            } else {
                // Copy bytes into value until a newline is hit
                while (*current != '\n' && *current != '\0') {

                    printf("%c", *current);
                    current++;
                }
                strlcpy(value, start, (int)(current - start) + 1);

                printf("\nFOUND Value: '%s'\n", value);

                // Now there should be a key and a value,
                // Attempt to put it into the struct

                if (strcmp(key, "title") == 0) {
                    char *title = malloc(sizeof(char) * strlen(value));
                    strcpy(title, value);
                    page->title = title;
                } else if (strcmp(key, "publish_date") == 0) {
                    char *publish_date = malloc(sizeof(char) * strlen(value));
                    strcpy(publish_date, value);
                    page->publish_date = publish_date;
                } else if (strcmp(key, "is_published") == 0) {
                    char *is_published = malloc(sizeof(char) * strlen(value));
                    strcpy(is_published, value);
                    page->is_published = is_published;
                } else if (strcmp(key, "slug") == 0) {
                    char *slug = malloc(sizeof(char) * strlen(value));
                    strcpy(slug, value);
                    page->slug = slug;
                } else if (strcmp(key, "description") == 0) {
                    char *description = malloc(sizeof(char) * strlen(value));
                    strcpy(description, value);
                    page->description = description;
                } else if (strcmp(key, "tags") == 0) {
                    printf("CANT DEAL WITH TAGS YET\n");
                    // char *publish_date = malloc(sizeof(char) *
                    // strlen(value)); page.publish_date = publish_date;
                }
            }
        }

    } while (in_frontmatter);

    // Success!
    return true;
}

/*
---
title: New year, same me?
publish_date: 2026-01-16
is_published: true
slug: 2026-new-year
description: My new years resolution for 2026
tags:
  - new-years-resolution
  - personal
---
*/
