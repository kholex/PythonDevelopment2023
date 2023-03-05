#!/usr/bin/env python3

import sys
import readline
import rlcompleter
import shlex
import cmd
from cowsay import list_cows, make_bubble, cowsay, cowthink, Option, COW_PEN, THOUGHT_OPTIONS

class cmdline(cmd.Cmd):
    intro = "Hellow!"
    promt = ">>> "
    def do_list_cows(self, args):
        command_args = shlex.split(args)
        cows = list_cows(command_args[0] if len(command_args) else COW_PEN)
        for cow in cows:
            print(cow)

    def help_list_cows(self):
        help_text = """
        Lists all cow file names in the given directory
        """
        print(help_text)

    def do_make_bubble(self, args):
        command_args = shlex.split(args)
        default_args_values = {
            "-b": "cowsay",
            "-d": 40,
            "-wt": True
        }
        if "-b" in command_args:
            ind = command_args.index("-b")
            value = command_args[ind + 1]
            default_args_values["-b"] = value

        if "-d" in command_args:
            ind = command_args.index("-d")
            value = command_args[ind + 1]
            default_args_values["-d"] = int(value)

        if "-wt" in command_args:
            ind = command_args.index("-w")
            value = command_args[ind + 1]
            default_args_values["-wt"] = bool(value)

        print(make_bubble(command_args[0],
                             brackets=THOUGHT_OPTIONS[default_args_values["-b"]],
                             width=default_args_values["-d"],
                             wrap_text=default_args_values["-w"]))
    def help_make_bubble(self):
        help_text = """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows
        :param brackets: -b
        :param width: -d
        :param wrap_text: -wt
        """
        print(help_text)

    def complete_make_bubble(self, pfx, line, beg, end):
        command_args = shlex.split(line)
        key, command = command_args[-2], command_args[-1]
        complete_args_values = {"-b": ["cowsay", "cowthink"],
                                "-wt": ["True", "False"]}
        if key in complete_args_values:
            return [s for s in complete_args_values[key] if s.startswith(command)]
        elif command in complete_args_values:
            return complete_args_values[command]
        else:
            return []

    def do_cowsay(self, args):
        command_args = shlex.split(args)
        default_args_values = {"-e": "oo",
                               "-c": "default",
                               "-T": "  "}
        if "-e" in command_args:
            ind = command_args.index("-e")
            value = command_args[ind + 1]
            default_args_values["-e"] = value

        if "-c" in command_args:
            ind = command_args.index("-c")
            value = command_args[ind + 1]
            default_args_values["-c"] = value

        if "-T" in command_args:
            ind = command_args.index("-w")
            value = command_args[ind + 1]
            default_args_values["-T"] = value

        print(cowsay(command_args[0],
                     cow=default_args_values["-c"],
                     eyes=default_args_values["-e"],
                     tongue=default_args_values["-T"]))

    def complete_cowsay(self, pfx, line, beg, end):
        command_args = shlex.split(line)
        key, command = command_args[-2], command_args[-1]
        complete_args_values = {"-e": ["oo", "LL", "oO"],
                                   "-c": list_cows(),
                                   "-T": ["  ", "&&"]}
        if key in complete_args_values:
            return [s for s in complete_args_values[key] if s.startswith(command)]
        elif command in complete_args_values:
            return complete_args_values[command]
        else:
            return []
    def help_cowsay(self):
        help_text = '''
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string
        :param message: The message to be displayed
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        '''
        print(help_text)

    def do_cowthink(self, args):
        command_args = shlex.split(args)
        default_args_values = {"-e": "oo",
                               "-c": "default",
                               "-T": "  "}
        if "-e" in command_args:
            ind = command_args.index("-e")
            value = command_args[ind + 1]
            default_args_values["-e"] = value

        if "-c" in command_args:
            ind = command_args.index("-c")
            value = command_args[ind + 1]
            default_args_values["-c"] = value

        if "-T" in command_args:
            ind = command_args.index("-w")
            value = command_args[ind + 1]
            default_args_values["-T"] = value

        print(cowthink(command_args[0],
                       cow=default_args_values["-c"],
                       eyes=default_args_values["-e"],
                       tongue=default_args_values["-T"]))

    def complete_cowthink(self, pfx, line, beg, end):
        command_args = shlex.split(line)
        key, command = command_args[-2], command_args[-1]
        complete_args_values = {"-e": ["oo", "LL", "oO"],
                                   "-c": list_cows(),
                                   "-T": ["  ", "&&"]}
        if key in complete_args_values:
            return [s for s in complete_args_values[key] if s.startswith(command)]
        elif command in complete_args_values:
            return complete_args_values[command]
        else:
            return []
    def help_cowthink(self):
        help_text = """
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string
        :param cow: -f – the available cows can be found by calling list_cows
        :param eyes: -e or eye_string
        :param tongue: -T or tongue_string
        """
        print(help_text)

    def do_exit(self, args):
        return 1

    def help_exit(self):
        print('Exit from command line')

    def emptyline(self):
        pass

    def do_EOF(self, line):
        return True

if __name__ == "__main__":
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    cmdline().cmdloop()