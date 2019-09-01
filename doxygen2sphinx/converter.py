"""A class for managing the conversion of dot graphs.


"""


import glob
import os

from .dotfile import Dotfile


class Converter(object):
    """A class for managing the conversion of dot graphs.

    Parameters
    ----------
    doxygen_dir : str
        The root directory of the Doxygen documentation
    sphinx_dir : str
        The directory where the converted dot graphs will be saved

    """
    def __init__(self, doxygen_dir, sphinx_dir):
        self.doxygen_dir = doxygen_dir
        self.sphinx_dir = sphinx_dir
        self.digraphs = {}
        self.dotfiles = []
        self.urls = {}

    def _get_attributes(self):
        """Find the .dot files in ``self.doxygen_dir`` and fill in the ``self.digraphs`` attribute."""
        dot_files = glob.glob(self.doxygen_dir + '/**/*.dot', recursive=True)
        self.dotfiles = [Dotfile(df) for df in dot_files]
        self.digraphs = {d.hash: d.digraph for d in self.dotfiles}

        html_files = [os.path.basename(html_file)[:-5] for html_file in glob.glob(self.sphinx_dir + '/build/html/*.html')]
        self.urls = {d.hash: d.get_url(html_files) for d in self.dotfiles}

    def convert(self):
        """Convert all of the .dot files from Doxygen format to Sphinx format."""
        self._get_attributes()

        html_files = [os.path.basename(html_file)[:-5] for html_file in glob.glob(self.sphinx_dir + '/build/html/*.html')]
        print(html_files)
        for df in self.dotfiles:
            outfile = os.path.join(self.sphinx_dir, 'source', '_static', '{0}.{1}.dot'.format(df.digraph, 'CALLER_GRAPH' if df.infile.endswith('icgraph.dot') else 'CALL_GRAPH'))
            df.convert(outfile)
