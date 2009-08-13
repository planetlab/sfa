import os, time

class Command:
    options = []
    help = ''
    type='command'
    matches = False
    targets = False
    action = 'store_const'

    def __init__(self):
        return

    def call(self, coptions, moptions, toptions):
        # Override this function
        return True

    def __call__(self, coption, moptions, toptions):
        return self.call(coptions,moptions,toptions)
