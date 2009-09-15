import os, time

class Command:
    options = []
    help = ''
    type='command'
    matches = False
    targets = False
    action = 'store_const'

    def __init__(self):
        self.options = []
        self.help = ''
        self.type = 'command'
        self.matches = False
        self.targets = False
        self.action = 'store_const'

        return

    def call(self, coptions, moptions, toptions):
        # Override this function
        return True

    def __call__(self, coptions, moptions, toptions):
        return self.call(coptions,moptions,toptions)
