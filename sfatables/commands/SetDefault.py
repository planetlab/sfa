import os, time
from sfatables.command import Command

class SetDefault(Command):
    options = [('-P','--default')]
    help = 'Set the default rule for a chain'
    key='set_default_rule'
    matches = False
    targets = False

    def __init__(self):
        return

    def call(self):
        # Override this function
        return True

    def __call__(self, option, opt_str, value, parser, *args, **kwargs):
        return self.call(option)
