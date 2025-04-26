import markdown
import sys

read_path = sys.argv[1]
write_path = sys.argv[2]

assert read_path, "Read file path and write file path not included!"
assert write_path, "Write file path not included!"

with open(read_path, 'r') as f:
    text = f.read()
    print('Markdown:')
    print(text)
    html = markdown.markdown(text)
    print('HTML:')
    print(html)

with open(write_path, 'w') as f:
    f.write(html)

