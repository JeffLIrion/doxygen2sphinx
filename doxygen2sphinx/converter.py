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
            # outfile = '{0}.html#{1}'.format(_get_longest_match(df.digraph, html_files), df.digraph)
            outfile = os.path.join(self.sphinx_dir, 'source', '_static', '{0}.{1}.dot'.format(df.digraph, 'CALL_GRAPH' if df.infile.endswith('cgraph.dot') else 'CALLER_GRAPH'))
            df.convert(outfile)
            # print('\n{0}\n{1}\n{2}\n\n'.format(outfile, '-'*len(outfile), '\n  '.join(result.split())))
            # print(result)


'''def _get_longest_match(digraph, html_files):
    """Find the longest match between ``digraph`` and the contents of ``html_files``.

    Parameters
    ----------
    digraph : str
        The ``digraph`` attribute of a `Dotfile` object
    html_files : list
        A list of the Sphinx html files

    Returns
    -------
    str
        The html file with the longest match with ``digraph``

    """
    print(digraph)
    print(html_files)
    max_match_len = 0
    len_max_match = 0
    longest_match = None

    for html_file in html_files:
        for i, (d, ht) in enumerate(zip(digraph, html_file)):
            if d != ht or i == len(html_file)-1:
                if i > max_match_len or (i == max_match_len and len(html_file) < len_max_match):
                    longest_match = html_file
                    max_match_len = i
                    len_max_match = len(html_file)
                break

    return longest_match'''
