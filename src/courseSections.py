import os
from natsort import natsorted


class CourseSection():

    def __init__(self, folder_path):
        self.folder_path = folder_path

    def all_sections(self):
        folders = natsorted(os.scandir(self.folder_path),
                            key=lambda x: x.name, reverse=True)
        sections = []
        for folder in folders:
            if folder.is_dir():
                sections.append({'name': folder.name, 'path': folder.path})
        return sections
