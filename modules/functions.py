from wordscraper import *


def regex_checker(searchwords):
    # Opens a txt file and searches it for keywords, ignoring stopwords.
    # It returns a nested dictionary with the searchwords as outer keys,
    # the page number as inner keys, and lists of sentences as the inner values

    # First, match the case of the searchwords and the text file. Then see if any
    # searchwords exist in the text.
    # re_searchwords = []
    for searchword in searchwords:
        print(searchword, end=", type:")
        print(type(searchword))
        print("Searchword is string? ", end="")
        print(type(searchword) is str)
        print("Searchword is pattern? ", end="")
        print(type(searchword) is re.Pattern)
        print()


def range_border(ws, cell_range, bstyle="thin"):

    rows = ws[cell_range]

    numrows = len(rows)
    numcols = len(rows[0])

    # Borders on the corners
    if numrows == 1:
        if numcols == 1:

            rows[0][0].border = Border(
                left=Side(style=bstyle),
                top=Side(style=bstyle),
                bottom=Side(style=bstyle),
                right=Side(style=bstyle),
            )
        else:
            rows[0][0].border = Border(
                left=Side(style=bstyle),
                top=Side(style=bstyle),
                bottom=Side(style=bstyle),
            )
            rows[0][-1].border = Border(
                right=Side(style=bstyle),
                top=Side(style=bstyle),
                bottom=Side(style=bstyle),
            )
    else:
        if numcols == 1:

            rows[0][0].border = Border(
                left=Side(style=bstyle),
                top=Side(style=bstyle),
                right=Side(style=bstyle),
            )
            rows[-1][0].border = Border(
                left=Side(style=bstyle),
                bottom=Side(style=bstyle),
                right=Side(style=bstyle),
            )
        else:
            rows[0][0].border = Border(left=Side(style=bstyle), top=Side(style=bstyle))
            rows[0][-1].border = Border(
                right=Side(style=bstyle), top=Side(style=bstyle)
            )
            rows[-1][0].border = Border(
                left=Side(style=bstyle), bottom=Side(style=bstyle)
            )
            rows[-1][-1].border = Border(
                right=Side(style=bstyle), bottom=Side(style=bstyle)
            )

    # Borders on left and right
    if numrows > 2:
        for row in rows[1:-1]:
            if numcols == 1:
                row[0].border = Border(
                    left=Side(style=bstyle), right=Side(style=bstyle)
                )
            else:
                row[0].border = Border(left=Side(style=bstyle))
                row[-1].border = Border(right=Side(style=bstyle))

    # # Border on top and botton
    if numcols > 2:
        if numrows == 1:
            for col in rows[0][1:-1]:
                col.border = Border(top=Side(style=bstyle), bottom=Side(style=bstyle))
        else:
            for col in rows[0][1:-1]:
                col.border = Border(top=Side(style=bstyle))
            for col in rows[-1][1:-1]:
                col.border = Border(bottom=Side(style=bstyle))


def col2num(col_str):
    """ Convert base26 column string to number. """
    expn = 0
    col_num = 0
    for char in reversed(col_str):
        col_num += (ord(char) - ord("A") + 1) * (26 ** expn)
        expn += 1

    return col_num


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


text_replacements = [
    ("-", " "),
    (":", " : "),
    ("´", ""),
    ("“", " "),
    ("/", " / "),
    ("‘", " "),
    ("%", " % "),
    ("’", " "),
    ("‐", " "),
    ("”", " "),
    ("g 20", "g20"),
    ("g 7", "g7"),
    ("***", " "),
    ("**", " "),
    ("*", " "),
    ("·", " "),
    ("***", " "),
    ("_", " "),
    ("‑", ""),
]


def text_fixer(text):
    # Takes some text and applies a series of transformations to make it readable - strips out problem punctuation,
    # puts spaces between adjacenet letters and numbers, removes hyphens

    global text_replacements

    # Add space between letters and adjacent numbers
    text = re.sub(r"([0-9]+(\.[0-9]+)?)", r" \1 ", text).strip()

    # Apply all text replcements from list
    for correction in text_replacements:
        text = text.replace(correction[0], correction[1])

    # Iterate through to delete long whitespaces
    for i in range(20):
        text = text.replace("  ", " ")

    return text
