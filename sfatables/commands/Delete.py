import os, time

class Command:
    options = []
    help = ''
    key=''
    matches = False
    targets = False

    def __init__(self):
        return

    def call(self):
        # Override this function
        return True

    def __call__(self, option, opt_str, value, parser, *args, **kwargs):
        return self.call(option)
