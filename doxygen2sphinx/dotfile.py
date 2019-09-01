"""Convert a single dot file from Doxygen format to Sphinx format.

"""


import re


REGEX_DIGRAPH = re.compile(r'digraph "(?P<digraph>[\S]+)"')
REGEX_URL = re.compile(r'URL="(?P<url>[\S]+)"')
REGEX_HASH = re.compile(r'xhtml#(?P<hash>[\S]+)')


class Dotfile(object):
    """Read, convert, and write dot files generated by Doxygen.

    Parameters
    ----------
    infile : str
        The .dot file that will be loaded

    """
    def __init__(self, infile):
        self.infile = infile
        self.hash = infile.split('_')[-2]
        self.url = None
        with open(self.infile) as f:
            for line in f.readlines():
                matches = REGEX_DIGRAPH.search(line)
                if matches:
                    self.digraph = matches.group('digraph')
                    break

    def __eq__(self, other):
        return self.infile == other.infile and self.hash == other.hash and self.digraph == other.digraph

    def convert(self, outfile, hashes):
        """Convert the URLs from Doxygen format to Sphinx format.

        Parameters
        ----------
        outfile : str
            Where the converted .dot file will be saved
        hashes : dict
            A dictionary where the keys are the hashes and the values are the `Dotfile` objects

        """
        with open(self.infile) as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'URL=' in line:
                    lines[i] = _replace_url(line, hashes)

            with open(outfile, 'w') as g:
                g.write(''.join(lines))

    def get_url(self, html_files):
        """Get the Sphinx URL that corresponds to the ``digraph`` attribute.

        Parameters
        ----------
        html_files : list
            A list of the Sphinx html files

        Returns
        -------
        str
            The Sphinx URL that corresponds to the ``digraph`` attribute

        """
        html_file = _get_longest_match(self.digraph, html_files)

        if html_file:
            self.url = '../{0}.html#{1}'.format(html_file, self.digraph)
        else:
            self.url = None
        return self.url

    def _replace_url(self, line):
        """Replace the Doxygen URL in ``line`` with Sphinx URLs.

        Parameters
        ----------
        line : str
            The line in the dot file

        """
        matches = REGEX_URL.search(line)
        if matches:
            url = matches.group('url')
            if self.url:
                return line.replace(url, self.url)

            return line.replace(', URL="', ',URL="').replace(',URL="{}"'.format(url), '')

        return line


def _get_longest_match(digraph, html_files):
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
    max_match_len = 0
    len_max_match = 0
    longest_match = None

    for html_file in html_files:
        for i, (d, ht) in enumerate(zip(digraph, html_file)):
            if d != ht or i == len(html_file) - 1:
                if i > max_match_len or (i == max_match_len and len(html_file) < len_max_match):
                    longest_match = html_file
                    max_match_len = i
                    len_max_match = len(html_file)
                break

    return longest_match


def _replace_url(line, hashes):
    """Replace the Doxygen URL in ``line`` with a Sphinx URL.

    Parameters
    ----------
    line : str
        The line in the dot file
    hashes : dict
        A dictionary where the keys are the hashes and the values are the `Dotfile` objects

    """
    matches = REGEX_URL.search(line)
    if matches:
        url = matches.group('url')

        hash_matches = REGEX_HASH.search(url)
        if hash_matches:
            hash_ = hash_matches.group('hash')
            dotfile = hashes.get(hash_)
            if dotfile and dotfile.url:
                return line.replace(url, dotfile.url)

        return line.replace(', URL="', ',URL="').replace(',URL="{}"'.format(url), '')

    return line
