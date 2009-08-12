import os, time
from sfa.sfatables.command import Add

class Add(Command):
    options = [('-A','--add')]
    help = 'Add a rule to a chain'
    key='add_rule'
    matches = False
    targets = False

    def __init__(self):
        return

    def call(self):
        # Override this function
        return True

    def __call__(self, option, opt_str, value, parser, *args, **kwargs):
        return self.call(option)
