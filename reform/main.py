#!/usr/bin/env python

from __future__ import print_function

import sys
import argparse

from .handlers import BaseInputHandler, BaseOutputHandler, BadLine

def parse_arguments(argv):
    known_inputs = BaseInputHandler.implementations()
    known_outputs = BaseOutputHandler.implementations()
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--on-error', choices=('exit', 'print', 'pass'), default='exit')
    parser.add_argument('-k', '--key-value', action='store_true', help="output key=value lines")
    parser.add_argument('-i', '--input-format', choices=known_inputs, default='csv')
    parser.add_argument('-o', '--output-format', choices=known_outputs, default='spaced')
    parser.add_argument('keys', nargs='+')
    options = parser.parse_args(argv[1:])
    options.input_format = known_inputs[options.input_format]
    options.output_format = known_outputs[options.output_format]
    return options

def main(options):
    input_handler = options.input_format(sys.stdin)
    output_handler = options.output_format(options.keys)
    for index, obj in input_handler:
        try:
            try:
                sys.stdout.write(output_handler.handle(index, obj) + '\n')
                sys.stdout.flush()
            except IOError:
                raise SystemExit(1) # presumably broken pipe
        except BadLine, error:
            if options.on_error == 'exit':
                raise SystemExit(str(error))
            elif options.on_error == 'print':
                sys.stderr.write("%s\n" % (error,))
            # fall through to next iteration

def baremain():
    return main(parse_arguments(sys.argv))

if __name__ == '__main__':
    baremain()
