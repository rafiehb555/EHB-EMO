#!/usr/bin/env python3
"""
Auto Markdown Fixer - Continuous Monitoring
"""

import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md'):
            print(f"Markdown file modified: {event.src_path}")
            # Auto-fix the file
            subprocess.run(["python", "markdown_fix_ultimate.py", "--fix-file", event.src_path])

def start_monitoring():
    event_handler = MarkdownHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_monitoring()
