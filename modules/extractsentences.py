from wordscraper import *


def page_search(txtfile, searchwords, page_num, stop_words=[]):
    # Opens a txt file and searches it for keywords, ignoring stopwords.
    # It returns a nested dictionary with the searchwords as outer keys,
    # the page number as inner keys, and lists of sentences as the inner values

    # First, match the case of the searchwords and the text file. Then see if any
    # searchwords exist in the text.
    re_searchwords = [re.compile(r"\b" + w + r"\b", re.IGNORECASE) for w in searchwords]

    try:
        text = open(txtfile, "r", encoding="utf8").read()
    except:
        text = open(txtfile, "r", encoding="ISO-8859-1").read()
    number_searchwords = 0

    for pattern in re_searchwords:
        matches = pattern.findall(text)
        number_searchwords += len(matches)

    searchwords_present = number_searchwords > 0

    # Create the dictionary
    page_sentences = {}
    page_key = "Page " + str(page_num)
    for searchword in searchwords:
        page_sentences[searchword] = {page_key: []}

    # If none of the searchwords are present, return a dictionary with empty keys
    if not searchwords_present:
        return page_sentences
    # Otherwise the remainder of code will run and extract sentences containing searchwords

    # # Convert the text to lower case
    low_text = text.lower().strip()
    low_text = re.sub(r"\([^)]*\)", "", low_text)
    low_text = re.sub(r"\-", "", low_text)

    # Temporarily replace stopwords with placeholders
    swl = [sw.lower() for sw in stop_words]
    phw = ["plhwd{0}".format(i) for i in range(len(swl))]
    for i in range(len(swl)):
        low_text = low_text.replace(swl[i], phw[i])

    for searchword in searchwords:
        low_text = low_text.replace(searchword, searchword.upper())

    # # Make all searchwords in the text upper case to emphasise them in the resulting doc
    for searchword in searchwords:
        low_text = low_text.replace(searchword.lower(), searchword.upper())

    re_sentences = [
        re.compile(r"[^.]*\b" + w + r"\b[^.]*\.", re.IGNORECASE) for w in searchwords
    ]

    for i in range(len(searchwords)):
        matches = re_sentences[i].findall(low_text)
        for j in range(len(matches)):
            for k in range(len(phw)):
                matches[j] = matches[j].replace(phw[k], swl[k])

        if len(matches) > 0:
            page_sentences[searchwords[i]][page_key] = matches

    return page_sentences


def doc_search(dir_path, searchwords, stop_words=[]):
    # Searches for the sentences containing keywords in all of the txt files
    # in a given directory. Returns a nested dictionary with the searchwords as outer keys,
    # the page number as inner keys, and lists of sentences as the inner values
    #
    # This prcoedure creates a dictionary for each page by calling the page_search procedure
    # and amalgamtes them all into a single dictionary

    # Create lists: txtfiles to read, page numbers, and pagenum keys for dictionary
    filenames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    page_nums = [f.replace(".txt", "").replace("page_", "") for f in filenames]
    page_keys = ["Page " + pn for pn in page_nums]

    # Initialize the dictionary that will store results, with 0 totals of each word
    doc_sentences = {}
    for searchword in searchwords:
        doc_sentences[searchword] = {"Total": 0}

    # Iterate through the txtfiles in the dir by pagenumber creating wordcount dictionaries
    # for that page then adding results to the parent document dictionary
    for page_num in page_nums:
        txtfile = dir_path + filenames[page_nums.index(page_num)]
        page_key = page_keys[page_nums.index(page_num)]
        page_dictionary = page_search(
            txtfile, searchwords, page_num, stop_words=stop_words
        )
        for searchword, value in page_dictionary.items():
            page_list = value[page_key]
            if len(page_list) != 0:
                doc_sentences[searchword][page_key] = page_list
                doc_sentences[searchword]["Total"] += len(page_list)

                # for sentence in list:
                #     doc_sentences[searchword]["Total"] += 1

    # Create a list of searchwords with no results
    keys_to_delete = []
    for searchword in searchwords:
        if len(doc_sentences[searchword]) == 0:
            keys_to_delete.append(searchword)

    # Delete the searchwords with no results from the dictionary
    for key in keys_to_delete:
        del doc_sentences[key]

    return doc_sentences


def delete_paragraph(paragraph):
    # Deletes paragraphs using docx

    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


def write_doc(
    input_dir, results_dir, searchwords, stop_words=[], project_name="Results"
):
    # Writes the sentences containing keywords to an existing a word document
    # with a Level 1 header for the doc name, Level 2 for each searchword
    # and level 3 for each page that has sentences containing it

    # Construct the string for the filename + time and its filepath
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M")
    project_filename = project_name + "_" + dt_string + ".docx"
    filepath = results_dir + project_filename

    # Create a list of the txtfile folders from their parent dir
    subdir_list = [x[0] for x in os.walk(input_dir)]
    subdir_list.remove(input_dir)
    filename_list = [x.replace(input_dir, "") for x in subdir_list]
    subdir_list = [x + "\\" for x in subdir_list]
    # Reverse it so newer docs get done first
    subdir_list = subdir_list.reverse()

    # Create the document and write its title
    document = Document()
    p = document.add_paragraph("Searchword Results")
    p.style = document.styles["Title"]

    # For each txtfile folder, create a wordsearch dictionary, a header in the word doc
    # for the filename, subheaders for searchwords, and text for the sentences
    for subdir in subdir_list:
        total_searchwords_count = 0
        # print("\n", subdir)
        txtfile_dict = doc_search(subdir, searchwords, stop_words)
        filename = filename_list[subdir_list.index(subdir)]
        filename_para = document.add_paragraph(filename)
        filename_para.style = document.styles["Heading 1"]

        # Report the search results
        for searchword, results in txtfile_dict.items():
            searchword_count = results["Total"]
            if searchword_count == 0:
                continue
            total_searchwords_count += searchword_count
            searchword_header = searchword + ": " + str(searchword_count)
            del txtfile_dict[searchword]["Total"]
            p = document.add_paragraph(searchword_header)
            p.style = document.styles["Heading 2"]

            for pagenum, result_list in results.items():
                pagenum_para = document.add_paragraph(pagenum)
                pagenum_para.style = document.styles["Heading 3"]
                for sentence in result_list:
                    if len(sentence) != 0:
                        try:
                            p = document.add_paragraph(sentence)
                        except:
                            p = document.add_paragraph(
                                "<<Unable to add this sentence - format conversion error>>"
                            )
                        p.style = document.styles["Normal"]
                    else:
                        delete_paragraph(pagenum_para)

        if total_searchwords_count == 0:
            delete_paragraph(filename_para)

    document.save(filepath)
    print("Sentences Extracted to " + project_filename + " in results folder")
