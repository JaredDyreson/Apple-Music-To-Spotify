#!/usr/bin/env python3.5
class FileHandler():
    def __init__(self, path=None):
        self.path = path
    def is_open(self):
        try:
            if self.path != None:
                fh = open(self.path, 'r')
                fh.close()
                return True
        except FileNotFoundError or self.path == None:
            return False
