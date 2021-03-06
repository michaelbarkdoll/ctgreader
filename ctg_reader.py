#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import json

PGN_HEADERS_REGEX = re.compile(r"\[([A-Za-z0-9_]+)\s+\"(.*)\"\]")


class CTGReader:
    def __init__(self, engine=''):
        if not engine:
            engine = './ctg_reader'
        self.engine = engine
        self.book = ''

    def open(self, book):
        '''Open a CTG file'''
        if not os.path.isfile(book):
            raise NameError("File {} does not exist".format(book))
        book = os.path.normcase(book)
        self.book = book

    def find(self, fen):
        '''Find all games with positions equal to fen'''
        if not self.book:
            raise NameError("Unknown CTG DB, first open a CTG file")
        cmd = "'{}' '{}'".format(self.book, fen)
        p = subprocess.Popen([self.engine, self.book, fen], stdout=subprocess.PIPE)
        return json.loads(p.stdout.read().decode())

def process_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-file', '--file', type=str, help="Name of the CTG book")
    parser.add_argument('-fen', '--fen', type=str, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", help='FEN position to query')
    settings = vars(parser.parse_args())
    return settings


if __name__ == '__main__':
    settings = process_arg()
    c = CTGReader()
    # print(settings)
    if settings['file']:
        c.open(settings['file'])
        print(c.find(settings['fen']))
    else:
        print('--file is required')