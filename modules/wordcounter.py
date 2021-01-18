from wordscraper import *


def entries_on_page(txtfile, searchwords, stop_words=[]):
    # Opens a txt file and searches it for keywords, ignoring stopwords.
    # It returns a dictionary with the searchwords as keys and their
    # count as values

    # First, match the case of the searchwords and the text file. Then see if any
    # searchwords exist in the text.
    re_searchwords = [re.compile(r"\b" + w + r"\b", re.IGNORECASE) for w in searchwords]

    # Open the text file - try different encoding formats
    try:
        text = open(txtfile, "r", encoding="utf8").read()
    except:
        text = open(txtfile, "r", encoding="ISO-8859-1").read()

    # Convert the text to lower case
    text = text.lower().strip()
    low = re.sub(r"\([^)]*\)", "", text)

    # Remove the stopwords
    sw_low = [sw.lower() for sw in stop_words]
    for sw in sw_low:
        text = text.replace(sw, "")

    # Initialise the dictionary and populate it with wordcounts
    count_dict = {}

    for searchword in searchwords:
        pattern = re_searchwords[searchwords.index(searchword)]
        matches = pattern.findall(text)
        count_dict[searchword] = len(matches)

    return count_dict


def entries_in_doc(input_dir, searchwords, stop_words=[]):
    # Takes an input directory, assumed filled with single page text files, and
    # returns a dictionary with Filename, page count, and count of each search term

    # Get document name and filenames to work on
    path = pathlib.PurePath(input_dir)
    doc_name = path.name
    filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]

    # Initialise the dictionary and populate it with page counts
    doc_count_dict = {"Document": doc_name, "Pages": len(filenames)}
    for filename in filenames:
        filepath = input_dir + "\\" + filename
        pagecount_dict = entries_on_page(filepath, searchwords, stop_words)
        for searchword in searchwords:
            if searchword not in doc_count_dict:
                doc_count_dict[searchword] = pagecount_dict[searchword]
            else:
                doc_count_dict[searchword] += pagecount_dict[searchword]

    return doc_count_dict


def entries_in_dir(
    input_dir, results_dir, searchwords, stop_words=[], project_name="Results"
):

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
    subdir_list = subdir_list.reverse()

    dir_dict = {"Document": [], "Pages": []}
    for searchword in searchwords:
        dir_dict[searchword] = []

    # print(dir_count_dict)
    for subdir in subdir_list:
        filename = filename_list[subdir_list.index(subdir)]
        doc_dict = entries_in_doc(subdir, searchwords, stop_words)
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

    # # Format the header
    # highlight = NamedStyle(name="highlight")
    # highlight.font = Font(bold=True, color="FFFFFF")
    # bd = Side(style="thick", color="000000")
    # highlight.border = Border(left=bd, top=bd, right=bd, bottom=bd)
    # highlight.fill = PatternFill("solid", fgColor="808080")

    # count = 0
    # for col in ws.iter_cols(min_col=2, min_row=2, max_col=6, max_row=2):
    #     col[count].style = highlight
    #     count += 1

    lastcol = chr(num_searchwords + 67)

    header1 = "B2:C2"
    header2 = "D2:" + lastcol + "2"
    body1 = "B2:C" + str(num_docs + 2)
    body2 = "D2:" + lastcol + str(num_docs + 2)

    range_border(ws, body1, bstyle="thin")
    range_border(ws, body2, bstyle="thin")
    range_border(ws, header1, bstyle="thin")
    range_border(ws, header2, bstyle="thin")

    # header1 = [ws.cell(row=2, column=i).value for i in range(2, 3)]

    # # cells = ws["B2":"C2"]
    # header1.font = Font(color="FF0000", size=20, italic=True)
    # header1.value = "Merged Cell"
    # header1.alignment = Alignment(horizontal="right", vertical="bottom")
    # header1.fill = GradientFill(stop=("000000", "FFFFFF"))  # 6 color hexadecimal system

    # Format column widths and wrap text
    ws.column_dimensions["B"].width = 70
    ws.column_dimensions["A"].width = 3.5
    ws.sheet_view.showGridLines = True
    ws.sheet_view.showGridLines = False

    wb.save(filepath)
    print("Wordcounts saved in " + project_filename + " in results folder")
