#!/usr/bin/python 
# SFAtables is a tool for restricting access to an SFA aggregate in a generic
# and extensible way. 

# It is modeled using abstractions in iptables. Specifically, 'matches' specify
# criteria for matching certain requests, 'targets' specify actions that treat
# requests in a certain way, and 'chains' are used to group related
# match-action pairs.

import sys
import os
import pdb
from optparse import OptionParser

def load_extensions(module):
    command_dict={}
    commands = __import__(module,fromlist=[".".join(module.split('.')[:-1])])

    for command_name in commands.all:
        command_module = getattr(commands, command_name)
        command = getattr(command_module, command_name)
        command_dict[command.key]=command()

    return command_dict

def create_parser(command_dict):
    parser = OptionParser(usage="sfatables [command] [chain] [match] [target]",
                             description='See "man sfatables" for more detail.')
    
    for k in command_dict.keys():
        command = command_dict[k]
        for (short_option,long_option) in command.options:
            parser.add_option(short_option,long_option,dest=command.key,help=command.help,metavar=command.help.upper())

    return parser


def main():
    command_dict = load_extensions("sfa.sfatables.commands")
    command_parser = create_parser(command_dict)
    (options, args) = command_parser.parse_args()

    if (len(options.keys() != 1):
        raise Exception("sfatables takes one command at a time.\n")

    selected_command = command_dict[options.keys()[0]]

    match_options = None
    target_options = None

    if (selected_command.matches):
        match_dict = load_extensions("sfa.sfatables.matches")
        match_parser = create_parser(match_dict)
        (options, args) = match_parser.parse_args(args[2:]) # Change to next location of --

    if (selected_command.targets):
        match_dict = load_extensions("sfa.sfatables.targets")
        target_parser = create_parser(match_dict)
        (options, args) = target_parser.parse_args(args[5:]) # Change to next location of --

    command(options, match_options, target_options)

if __name__=='__main__':
    main()
