"""Unit tests for the doxygen2sphinx/dotfile.py module

"""


import os
import sys
import unittest
sys.path.insert(0, '..')

import doxygen2sphinx
from doxygen2sphinx.dotfile import Dotfile


CGRAPH = os.path.join(os.path.dirname(__file__), 'data', 'doxygen', 'd7', 'ddb', 'classadb_1_1adb__commands_1_1AdbCommands_a003266da034244516954809091e43666_cgraph.dot')
ICGRAPH = os.path.join(os.path.dirname(__file__), 'data', 'doxygen', 'd7', 'ddb', 'classadb_1_1adb__commands_1_1AdbCommands_a0e16b280f809807c126e5ea0ba0ce63b_icgraph.dot')

DOTFILES = {'d7/ddb/classadb_1_1adb__commands_1_1AdbCommands_a003266da034244516954809091e43666_cgraph.dot': Dotfile(CGRAPH),
            'd7/ddb/classadb_1_1adb__commands_1_1AdbCommands_a0e16b280f809807c126e5ea0ba0ce63b_icgraph.dot': Dotfile(ICGRAPH)}

DIGRAPHS = {'a003266da034244516954809091e43666': 'adb.adb_commands.AdbCommands.ConnectDevice',
            'a0e16b280f809807c126e5ea0ba0ce63b': 'adb.adb_commands.AdbCommands.StreamingShell'}

class TestDotfile(unittest.TestCase):
    def setUp(self):
        self.dotfile = Dotfile(CGRAPH)

    def test_init(self):
        self.assertEqual('adb.adb_commands.AdbCommands.ConnectDevice', self.dotfile.digraph)
        self.assertEqual('a003266da034244516954809091e43666', self.dotfile.hash)

    #def test_convert(self):
    #    converted = self.dotfile.convert({}, '')


if __name__ == '__main__':
    unittest.main()
