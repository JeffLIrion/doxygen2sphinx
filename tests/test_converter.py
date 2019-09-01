"""Unit tests for the doxygen2sphinx/converter.py module

"""


import os
import sys
import unittest
sys.path.insert(0, '..')

import doxygen2sphinx
from doxygen2sphinx.converter import Converter
from doxygen2sphinx.dotfile import Dotfile


DOXYGEN_DIR = os.path.join(os.path.dirname(__file__), 'data', 'doxygen')
#SPHINX_DIR = os.path.join(os.path.dirname(__file__), 'data', 'sphinx', 'source', '_static')
SPHINX_DIR = os.path.join(os.path.dirname(__file__), 'data', 'sphinx')

CGRAPH = os.path.join(os.path.dirname(__file__), 'data', 'doxygen', 'd7', 'ddb', 'classadb_1_1adb__commands_1_1AdbCommands_a003266da034244516954809091e43666_cgraph.dot')
ICGRAPH = os.path.join(os.path.dirname(__file__), 'data', 'doxygen', 'd7', 'ddb', 'classadb_1_1adb__commands_1_1AdbCommands_a0e16b280f809807c126e5ea0ba0ce63b_icgraph.dot')

DOTFILES = [Dotfile(CGRAPH), Dotfile(ICGRAPH)]

HASHES = {'a003266da034244516954809091e43666': Dotfile(CGRAPH),
          'a0e16b280f809807c126e5ea0ba0ce63b': Dotfile(ICGRAPH)}

class TestConverter(unittest.TestCase):
    def setUp(self):
        self.converter = Converter(DOXYGEN_DIR, SPHINX_DIR)

    def test_init(self):
        self.assertTrue(True)
        #self.assertEqual('adb.adb_commands.AdbCommands.ConnectDevice', self.dotfile.digraph)
        #self.assertEqual('a003266da034244516954809091e43666', self.dotfile.hash)

    def test_get_digraphs(self):
        self.converter._get_attributes()
        self.assertDictEqual(self.converter.hashes, HASHES)
        self.assertListEqual(sorted(self.converter.dotfiles, key=lambda x: x.infile), sorted(DOTFILES, key=lambda x: x.infile))

    def test_convert(self):
        self.converter.convert()


if __name__ == '__main__':
    unittest.main()
