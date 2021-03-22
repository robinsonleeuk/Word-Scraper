from wordscraper import *


def entries_on_page(
    txtfile, searchwords, reported_searchwords, searchword_patterns, stop_words=[]
):
    # Opens a txt file and searches it for keywords, ignoring stopwords.
    # It returns a dictionary with the searchwords as keys and their
    # count as values

    # Load the lists from lists module: spellchecks to ignore and text replacements to make_____________________________
    global text_replacements

    # Set criteria for ignoring a page__________________________________________________________________________________

    # Set variables, ignore_page, which is false by default, Becomes true if page is annex, glossary, etc
    # end_doc is triggered when the first words on a page indicate the procedure is finished with the doc (e.g. annex)
    ignore_page = False
    end_doc = False

    # Open the text file - try different encoding formats
    try:
        text = open(txtfile, "r", encoding="utf8").read()
    except:
        text = open(txtfile, "r", encoding="ISO-8859-1").read()

    # Take first hundred words to check for ignore or stop criteria
    first_hundred_list = text.split()[0:100]
    first_hundred_string = " ".join(first_hundred_list)

    # check if they contain 'Annex'
    annex_pattern = re.compile(r"^annex[:]*", re.IGNORECASE)
    annex_match = re.search(annex_pattern, first_hundred_string)

    if annex_match:
        ignore_page = True
        end_doc = True

    # Check if they are table of contents
    contents_pattern = re.compile(r"^contents", re.IGNORECASE)
    contents_match = re.search(contents_pattern, first_hundred_string)

    if contents_match:
        ignore_page = True

    # Convert the text to lower case
    text = text.lower().strip()
    # low = re.sub(r"\([^)]*\)", "", text)

    # Clean the text up - remove problem punctuation and enspace numbers adjacent to letters
    text = text_fixer(text)

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

    return count_dict, ignore_page, end_doc


def entries_in_doc(
    input_dir, searchwords, reported_searchwords, searchword_patterns, stop_words=[]
):
    # Takes an input directory, assumed filled with single page text files, and
    # returns a dictionary with Filename, page count, and count of each search term

    # Get document name and filenames to work on
    path = pathlib.PurePath(input_dir)
    doc_name = path.name
    filenames_unsorted = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    page_nums_unsorted = [
        f.replace(".txt", "").replace("page_", "") for f in filenames_unsorted
    ]

    page_ints = [int(p) for p in page_nums_unsorted]

    page_nums = []
    filenames = []
    for i in range(1, len(page_ints) + 1):
        page_nums.append(page_nums_unsorted[page_ints.index(i)])
        filenames.append(filenames_unsorted[page_ints.index(i)])

    # filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    # Initialise the dictionary and populate it with page counts
    doc_count_dict = {"Document": doc_name, "Pages": len(filenames), "Wordcount": 0}
    for filename in filenames:
        filepath = input_dir + "\\" + filename
        pagecount_dict, ignore_page, end_doc = entries_on_page(
            txtfile=filepath,
            searchwords=searchwords,
            reported_searchwords=reported_searchwords,
            searchword_patterns=searchword_patterns,
            stop_words=stop_words,
        )

        # If the page was one that triggers a document -end event, finish the procedure and return the dictionary
        if end_doc == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ended procedure")
            return doc_count_dict

        # If the page was one that should be ignored (annex, glossary), do not include it - move to next loop
        if ignore_page == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ignored")
            continue

        doc_count_dict["Wordcount"] += pagecount_dict["Wordcount"]
        for reported_searchword in reported_searchwords:
            if reported_searchword not in doc_count_dict:
                # print(reported_searchword)
                # print("Doc Dict: ", end="")
                # print(doc_count_dict)
                # print("Page Dict: ", end="")
                # print(pagecount_dict)
                # print()
                if reported_searchword not in pagecount_dict:
                    doc_count_dict[reported_searchword] = 0
                    continue
                doc_count_dict[reported_searchword] = pagecount_dict[
                    reported_searchword
                ]
            else:
                if reported_searchword in pagecount_dict:
                    doc_count_dict[reported_searchword] += pagecount_dict[
                        reported_searchword
                    ]

    return doc_count_dict


def entries_in_dir(
    input_dir,
    results_dir,
    searchwords,
    reported_searchwords,
    stop_words=[],
    project_name="Results",
):

    short_results_dir = results_dir.replace(os.getcwd(), "")

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
    filename_list = filename_list[::-1]
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
            reported_searchwords=reported_searchwords,
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
    print("Wordcounts saved in " + project_filename + " in " + short_results_dir)
