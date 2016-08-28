#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Add bookmarks into PDF

usage:
    ./add_bookmarks.py <pdf_in_filename> <bookmarks_filename> [pdf_out_filename]
    or
    ./add_bookmarks.py --test
"""

import os
import re
import codecs

from PyPDF2 import PdfFileWriter, PdfFileReader

__all__ = [
    'add_bookmarks'
]

__author__ = 'RussellLuo'
__version__ = '0.02'

def add_bookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename=None):
    """Add bookmarks into PDF

    Some useful references:
        [1] http://pybrary.net/pyPdf/
        [2] http://stackoverflow.com/questions/18855907/adding-bookmarks-using-pypdf2
        [3] http://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
    """
    pdf_out = PdfFileWriter()

    # copy `pdf_in` into `pdf_out`
    pdf_in = PdfFileReader(open(pdf_in_filename, 'rb'))
    numpages = pdf_in.getNumPages()
    for i in range(numpages):
        pdf_out.addPage(pdf_in.getPage(i))

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
        pdf_out_filename = name_parts[0] + '(new)' + name_parts[1]

    # save `pdf_out`
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
    print('in processing, please wait a moment...')
    try:
        bookmarks_tree = get_bookmarks_tree(bookmarks_filename)
        add_bookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename)
    except Exception as e:
        print('failed:\n    %s' % str(e))
    else:
        print('succeeded')

# documentation test
def doc_test():
    import doctest
    doctest.testmod()

# test
if __name__ == '__main__':
    import sys

    if len(sys.argv) not in (2, 3, 4):
        sys.stderr.write(__doc__)
        sys.exit(1)

    if sys.argv[1] == '--test':
        doc_test()
    else:
        run_script(*sys.argv[1:])
