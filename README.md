# PDFBookmarker

Add bookmarks into PDF using [PyPDF2][1].


## Installation

Install pdfbookmarker:

```bash
$ pip install pdfbookmarker
```

## Usage

1. Turn to your target PDF (e.g. `MyBook.pdf`), record bookmark titles and page
   numbers of the PDF into a TEXT file (e.g. `my_bookmarks.txt`) **by hand** 
   with the following format:

    ```
    <nested level>"<bookmark title>"|<page number>
    ```

    For samples, see [sample_bookmarks.txt](sample_bookmarks.txt). (Offsets are also
    supported, see [here](https://github.com/RussellLuo/pdfbookmarker/pull/7#issuecomment-711136889))

2. Generate a copy of `MyBook.pdf` with additional bookmarks file specified by
   `my_bookmarks.txt`:

    ```bash
    $ pdfbm MyBook.pdf my_bookmarks.txt
    ```

    An auto-detected, expected or suggested filename for bookmarks is `MyBook.txt`,
    when the input filenamne e.g. is `MyBook.pdf`.
    
    The default filename of the output PDF is `MyBook-new.pdf`; You, of course, can
    specify the filename explicitly:
    
    ```bash
    $ pdfbm MyBook.pdf my_bookmarks.txt MyBook_with_bookmarks.pdf
    ```


## License

[MIT][2]


[1]: https://github.com/mstamy2/PyPDF2
[2]: http://opensource.org/licenses/MIT
