#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Add bookmarks to existing PDF files

Usage:
  $ pdfbm [options] <FILE.pdf> [FILE.txt] [FILE-new.pdf]

Options:
  -h, --help    show this help

Examples:
  $ pdfbm FILE.pdf  # will read FILE.pdf as PDF, FILE.txt as a
  bookmarks file and shall give the FILE-new.pdf as output.

Hence, parameters FILE.txt and FILE-new.pdf are optional, hah.
"""

import codecs
import os
import re
import sys

from PyPDF2 import PdfFileMerger, PdfFileReader

__version__ = '0.5.0'
__author__ = 'RussellLuo'
__email__ = 'luopeng.he@gmail.com'
__license__ = 'MIT'


def add_bookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename=None):
    """Add bookmarks to existing PDF files

    Home:
        https://github.com/RussellLuo/pdfbookmarker

    Some useful references:
        [1] http://pybrary.net/pyPdf/
        [2] http://stackoverflow.com/questions/18855907/adding-bookmarks-using-pypdf2
        [3] http://stackoverflow.com/questions/3009935/looking-for-a-good-python-tree-data-structure
    """
    pdf_in = PdfFileReader(pdf_in_filename)

    # merge `pdf_in` into `pdf_out`, using PyPDF2.PdfFileMerger()
    pdf_out = PdfFileMerger()
    pdf_out.append(pdf_in, import_bookmarks=False)

    # copy/preserve existing document info
    doc_info = pdf_in.getDocumentInfo()
    if doc_info:
        pdf_out.addMetadata(doc_info)

    def crawl_tree(tree, parent):
        for title, page_num, subtree in tree:
            current = pdf_out.addBookmark(title, page_num, parent) # add parent bookmark
            if subtree:
                crawl_tree(subtree, current)

    # add bookmarks into `pdf_out` by crawling `bookmarks_tree`
    crawl_tree(bookmarks_tree, None)

    # get `pdf_out_filename` if it's not specified
    if not pdf_out_filename:
        name_parts = os.path.splitext(pdf_in_filename)
        pdf_out_filename = name_parts[0] + '-new' + name_parts[1]

    # write all data to the given file
    pdf_out.write(pdf_out_filename)
    pdf_out.close()

    return pdf_out_filename


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
            pluses, title, page_num = res.groups()
            cur_level = len(pluses)  # plus count stands for level
            cur_node = (title, int(page_num) - 1, [])

            if not (0 < cur_level <= prev_level + 1):
                raise Exception('plus (+) count is invalid here: %s' % line.strip())
            else:
                # append the current node into its parent node (with the level `cur_level` - 1)
                latest_nodes[cur_level - 1].append(cur_node)

            latest_nodes[cur_level] = cur_node[2]
            prev_level = cur_level

    return tree


# run as a script
def run_script(pdf_in_filename, bookmarks_filename, pdf_out_filename=None):
    sys.stderr.write('In processing, please wait...\n')
    try:
        bookmarks_tree = get_bookmarks_tree(bookmarks_filename)
        pdf_out_filename = add_bookmarks(pdf_in_filename, bookmarks_tree, pdf_out_filename)
    except Exception as exc:
        sys.stderr.write("error:\n%s\n" % str(exc))
    else:
        sys.stderr.write("New PDF generated: %s\n" % pdf_out_filename)


# documentation test
def doc_test():
    import doctest
    doctest.testmod()


# test and, or execute
def main():
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


if __name__ == '__main__':
    main()
