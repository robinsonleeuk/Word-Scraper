from wordscraper import *


def entries_on_page(txtfile, searchwords, searchword_patterns, stop_words=[]):
    # Opens a txt file and searches it for keywords, ignoring stopwords.
    # It returns a dictionary with the searchwords as keys and their
    # count as values

    # Load the lists from lists module: spellchecks to ignore and text replacements to make_____________________________
    global text_replacements

    global reported_searchwords

    # Open the text file - try different encoding formats
    try:
        text = open(txtfile, "r", encoding="utf8").read()
    except:
        text = open(txtfile, "r", encoding="ISO-8859-1").read()

    # Convert the text to lower case
    text = text.lower().strip()
    # low = re.sub(r"\([^)]*\)", "", text)

    # Clean the text up - remove problem punctuation and enspace numbers adjacent to letters
    text = text_fixer(text)

    # # Remove punctutation that stops word boundary recognition
    # for correction in text_replacements:
    #     text = text.replace(correction[0], correction[1])

    text = remove_stopwords(text)

    wordcount = len(text.split())

    # Remove the stopwords
    stopword_low = [stopword.lower() for stopword in stop_words]
    for stopword in stopword_low:
        text = text.replace(stopword, "")

    # Initialise the dictionary and populate it with wordcounts
    count_dict = {}

    count_dict["Wordcount"] = wordcount

    for searchword in searchwords:
        reported_searchword = reported_searchwords[searchwords.index(searchword)]
        pattern = searchword_patterns[searchwords.index(searchword)]
        matches = pattern.findall(text)
        count_dict[reported_searchword] = len(matches)

    return count_dict


def entries_in_doc(input_dir, searchwords, searchword_patterns, stop_words=[]):
    # Takes an input directory, assumed filled with single page text files, and
    # returns a dictionary with Filename, page count, and count of each search term

    # Get document name and filenames to work on
    path = pathlib.PurePath(input_dir)
    doc_name = path.name
    filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    global reported_searchwords

    # Initialise the dictionary and populate it with page counts
    doc_count_dict = {"Document": doc_name, "Pages": len(filenames), "Wordcount": 0}
    for filename in filenames:
        filepath = input_dir + "\\" + filename
        pagecount_dict = entries_on_page(
            txtfile=filepath,
            searchwords=searchwords,
            searchword_patterns=searchword_patterns,
            stop_words=stop_words,
        )
        doc_count_dict["Wordcount"] += pagecount_dict["Wordcount"]
        for reported_searchword in reported_searchwords:
            if reported_searchword not in doc_count_dict:
                doc_count_dict[reported_searchword] = pagecount_dict[
                    reported_searchword
                ]
            else:
                doc_count_dict[reported_searchword] += pagecount_dict[
                    reported_searchword
                ]

    return doc_count_dict


def entries_in_dir(
    input_dir, results_dir, searchwords, stop_words=[], project_name="Results"
):

    global reported_searchwords

    # Construct the string for the filename + time and its filepath
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M")
    project_filename = project_name + "_" + dt_string + ".xlsx"
    filepath = results_dir + project_filename

    # Create a list of the txtfile folders from their parent dir
    subdir_list = [x[0] for x in os.walk(input_dir)]
    subdir_list.remove(input_dir)
    filename_list = [x.replace(input_dir, "") for x in subdir_list]
    subdir_list = [x + "\\" for x in subdir_list]
    # Reverse it so newer docs get done first
    subdir_list = subdir_list[::-1]

    # Make regex patterns of searchwords for the doc and page search functions.
    # A list of patterns - just the words surrounded by word boundaries
    searchword_patterns = [
        re.compile(r"\b" + w + r"\b", re.IGNORECASE) for w in searchwords
    ]

    dir_dict = {"Document": [], "Pages": [], "Wordcount": []}
    for reported_searchword in reported_searchwords:
        dir_dict[reported_searchword] = []

    # print(dir_count_dict)
    for subdir in subdir_list:
        filename = filename_list[subdir_list.index(subdir)]
        doc_dict = entries_in_doc(
            input_dir=subdir,
            searchwords=searchwords,
            searchword_patterns=searchword_patterns,
            stop_words=stop_words,
        )
        for key, value in doc_dict.items():
            dir_dict[key].append(value)

    df = pd.DataFrame.from_dict(dir_dict)
    # print(df)
    rows = dataframe_to_rows(df)

    wb = Workbook()
    ws = wb.active
    ws.title = "Wordcounts"

    num_docs = len(subdir_list)
    num_searchwords = len(dir_dict) - 2
    # print(num_searchwords)

    # Fill in the workbook
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    # Delete and add cols and rows
    ws.delete_cols(1)
    ws.delete_rows(2)
    ws.insert_rows(1)
    ws.insert_cols(1)

    lastcol = colnum_string(num_searchwords + 3)

    header1 = "B2:D2"
    header2 = "E2:" + lastcol + "2"
    body1 = "B2:D" + str(num_docs + 2)
    body2 = "E2:" + lastcol + str(num_docs + 2)

    range_border(ws, body1, bstyle="thin")
    range_border(ws, body2, bstyle="thin")
    range_border(ws, header1, bstyle="thin")
    range_border(ws, header2, bstyle="thin")

    # Format column widths and wrap text
    ws.column_dimensions["B"].width = 70
    ws.column_dimensions["A"].width = 3.5
    ws.sheet_view.showGridLines = True
    ws.sheet_view.showGridLines = False

    wb.save(filepath)
    print("Wordcounts saved in " + project_filename + " in results folder")
