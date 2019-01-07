#!/usr/bin/env python3.5

import sqlite3
import os
import sys

class database():
    def __init__(self, path=None):
        self.path = path
        self.connection = sqlite3.connect(self.path)
    def connection(self):
        return self.connection
