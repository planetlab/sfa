import os, time
from sfatables.command import Command

class Add(Command):
    options = [('-A','--add')]
    help = 'Add a rule to a chain'
    matches = True
    targets = True

    def __init__(self):
        return

    def call(self, command_options, match_options, target_options):
        # Override this function
        return True

