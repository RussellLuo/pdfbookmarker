PdfBookmarker
=============

Add bookmarks into PDF using PyPDF2

1| Dependencies
---------------

To use the scripts here, you must install or download [PyPDF2][] first.

2| Usage
--------

1) Make `add_bookmarks.py` executable:

    $ chmod +x add_bookmarks.py

2) Turn to your target PDF (e.g. `MyBook.pdf`), record bookmark titles and page numbers of the PDF into a TEXT file (e.g. `my_bookmarks.txt`) **by hand** with the following format:

    <nested level><"bookmark title">|<page number>

For samples, see `sample_bookmarks.txt`.

3) Generate a copy of `MyBook.pdf` with additional bookmarks specified by `my_bookmarks.txt`:

    ./add_bookmarks.py MyBook.pdf my_bookmarks.txt

The default filename of the output PDF is `MyBook(new).pdf`. Of course you can specify the filename explicitly:

    ./add_bookmarks.py MyBook.pdf my_bookmarks.txt MyBook_with_bookmarks.pdf


[PyPDF2]: https://github.com/colemana/PyPDF2
