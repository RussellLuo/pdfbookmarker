#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Add bookmarks to existing PDF files

Usage:
  ./add_bookmarks.py [options] <FILE.pdf> [FILE.txt] [FILE-new.pdf]

Options:
  -h, --help    show this help

Examples:
  ./add_bookmarks.py FILE.pdf # will read FILE.pdf as PDF, FILE.txt as a
  bookmarks file and shall give the FILE-new.pdf as output.

Hence, parameters FILE.txt and FILE-new.pdf are optional, hah.

License GPLv3+: GNU/GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software, you are free to change and redistribute it.  There is
NO WARRANTY, to the extent permitted by law. Use it at your own risk!
"""

import os
import re
import codecs

from PyPDF2 import PdfFileMerger, PdfFileReader

__all__ = [
    'addBookmarks'
]

__author__ = 'RussellLuo'
__version__ = '0.03'

def addBookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename=None):
    """Add bookmarks to existing PDF files

    Home:
        https://github.com/RussellLuo/pdfbookmarker

    Some useful references:
        [1] http://pybrary.net/pyPdf/
        [2] http://stackoverflow.com/questions/18855907/adding-bookmarks-using-pypdf2
        [3] http://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
    """
    pdf_out = PdfFileMerger()

    # read `pdf_in` into `pdf_out`, using PyPDF2.PdfFileMerger()
    with open(pdf_in_filename, 'rb') as inputStream:
        pdf_out.append(inputStream, import_bookmarks=False)

    # copy/preserve existing metainfo
    pdf_in = PdfFileReader(pdf_in_filename)
    metaInfo = pdf_in.getDocumentInfo()
    if metaInfo:
        pdf_out.addMetadata(metaInfo)

    def crawl_tree(tree, parent):
        for title, pagenum, subtree in tree:
            current = pdf_out.addBookmark(title, pagenum, parent) # add parent bookmark
            if subtree:
                crawl_tree(subtree, current)

    # add bookmarks into `pdf_out` by crawling `bookmarks_tree`
    crawl_tree(bookmarks_tree, None)

    # get `pdf_out_filename` if it's not specified
    if not pdf_out_filename:
        name_parts = os.path.splitext(pdf_in_filename)
        pdf_out_filename = name_parts[0] + '-new' + name_parts[1]

    # wrie `pdf_out`
    with open(pdf_out_filename, 'wb') as outputStream:
        pdf_out.write(outputStream)

def get_bookmarks_tree(bookmarks_filename):
    """Get bookmarks tree from TEXT-format file

    Bookmarks tree structure:

        >>> get_bookmarks_tree('sample_bookmarks.txt')
        [(u'Foreword', 0, []), (u'Chapter 1: Introduction', 1, [(u'1.1 Python', 1, [(u'1.1.1 Basic syntax', 1, []), (u'1.1.2 Hello world', 2, [])]), (u'1.2 Exercises', 3, [])]), (u'Chapter 2: Conclusion', 4, [])]

    The above test result may be more readable in the following format:

        [
            (u'Foreword', 0, []),
            (u'Chapter 1: Introduction', 1,
                [
                    (u'1.1 Python', 1,
                        [
                            (u'1.1.1 Basic syntax', 1, []),
                            (u'1.1.2 Hello world', 2, [])
                        ]
                    ),
                    (u'1.2 Exercises', 3, [])
                ]
            ),
            (u'Chapter 2: Conclusion', 4, [])
        ]

    Thanks Stefan, who share us a perfect solution for Python tree.
    See http://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
    Since dictionary in Python is unordered, I use list instead now.

    Also thanks Caicono, who inspiring me that it's not a bad idea to record bookmark titles and page numbers by hand.
    See here: http://www.caicono.cn/wordpress/2010/01/%E6%80%9D%E8%80%83%E5%85%85%E5%88%86%E5%86%8D%E8%A1%8C%E5%8A%A8-python%E8%AF%95%E6%B0%B4%E8%AE%B0.html
    And I think it's the only solution for scan version PDFs to be processed automatically.
    """

    # bookmarks tree
    tree = []

    # the latest nodes (the old node will be replaced by a new one if they have the same level)
    # 
    # each item (key, value) in dictionary represents a node
    # `key`: the level of the node
    # `value`: the children list of the node
    latest_nodes = {0: tree}

    prev_level = 0
    for line in codecs.open(bookmarks_filename, 'r', encoding='utf-8'):
        res = re.match(r'(\+*)\s*?"([^"]+)"\s*\|\s*(\d+)', line.strip())
        if res:
            pluses, title, pagenum = res.groups()
            cur_level = len(pluses) # plus count stands for level
            cur_node = (title, int(pagenum) - 1, [])

            if not (cur_level > 0 and cur_level <= prev_level + 1):
                raise Exception('plus (+) count is invalid here: %s' % line.strip())
            else:
                # append the current node into its parent node (with the level `cur_level` - 1)
                latest_nodes[cur_level - 1].append(cur_node)

            latest_nodes[cur_level] = cur_node[2]
            prev_level = cur_level

    return tree

# run as a script
def run_script(pdf_in_filename, bookmarks_filename, pdf_out_filename=None):
    sys.stderr.write('processing, please wait ...')
    try:
        bookmarks_tree = get_bookmarks_tree(bookmarks_filename)
        addBookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename)
    except Exception as e:
        sys.stderr.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bfailed:         \n  %s\n" % str(e))
    else:
        sys.stderr.write("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\bdone!           \n")

# documentation test
def doc_test():
    import doctest
    doctest.testmod()

# test and, or execute
if __name__ == '__main__':
    import sys

    if len(sys.argv) not in (2, 3, 4) or sys.argv[1] in ('-h', '--help'):
        sys.stderr.write(__doc__)
        sys.exit(1)

    if sys.argv[1] in ('-t', '--test'):
        doc_test()
    elif len(sys.argv) == 2:
        name_parts = os.path.splitext(sys.argv[1])
        run_script(sys.argv[1], name_parts[0] + '.txt', pdf_out_filename=None)
    else:
        run_script(*sys.argv[1:])
