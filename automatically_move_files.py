# Downloads folder organizer
# Automatically move files from a folder to another,
# with some rules to handle destination by filename

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# pip install watchdog

import os
import json
import time


class MyDownloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            src  = folder_to_track + "/" + filename
            
            if filename[:7].lower() == "receipt" or filename[:6].lower() == "boleto":
                new_destination = folder_destination_receipts
            elif filename[-4:] == ".pdf":
                new_destination = folder_destination_documents
            else:
                #new_destination = folder_destination
                continue
            
            new_destination += "/" + filename
            os.rename(src, new_destination)


folder_to_track = "/home/alcsaw/Downloads"
folder_destination = "/home/alcsaw/Documents/test/"
folder_destination_documents = "/home/alcsaw/Documents"
folder_destination_receipts = "/home/alcsaw/Documents/Orders and Receipts"

event_handler = MyDownloadHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
