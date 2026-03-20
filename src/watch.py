# Thanks to this website
# https://www.geeksforgeeks.org/python/how-to-detect-file-changes-using-python/

import build_blog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def build_site():
    build_blog.main()
    print("\nWatching ...")


class UpdateHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            build_site()


# Create an observer and event handler
observer = Observer()
event_handler = UpdateHandler()

# Set up observer to watch a specific directory
dir_to_watch = "site"
observer.schedule(event_handler, dir_to_watch, recursive=True)

# Start the observer
observer.start()

# Build the site
build_site()


# Keep the script running
try:
    while observer.is_alive():
        observer.join(1)
except KeyboardInterrupt:
    observer.stop()

# Joins the background thread
observer.join()
