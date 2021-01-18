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
        # print("Searchword is string? ",end='')
        # print(type(searchword) is str)

        # if type(searchword) is str:
        #     print(searchword, end="")
        #     print(" = String")
        # elif type(searchword) == "re.Pattern":
        #     print(searchword, end="")
        #     print(" = Pattern")
        # else:
        #     print("Neither")
        #     print(type(searchword))

    # re_searchwords = [re.compile(r"\b" + w + r"\b", re.IGNORECASE) for w in searchwords]

    # for i in range(len(searchwords)):
    #     print("Searchword: ", end="")
    #     print(searchwords[i], end=", ")
    #     print("Regex: ", end="")
    #     print(re_searchwords[i])
    #     print(type(searchwords[i]), type(re_searchwords[i]))


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
