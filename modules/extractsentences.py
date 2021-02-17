from wordscraper import *


def page_search(
    txtfile,
    searchwords,
    searchword_patterns,
    searchsentence_patterns,
    page_num,
    stop_words=[],
):
    # Opens a txt file and searches it for search words, ignoring stopwords.
    # It returns a nested dictionary with the searchwords as outer keys,
    # the page number as inner keys, and lists of sentences containing the search words as the inner values

    # It take as arguments txtfile, which is the txt to be searched, a list of searchwords, regex patterns of these searchwords: a) the word itself surrounded by word boundaries, b) the sentence sontaining the word, the page number (for use in the dictionary) and stopwords

    # Load the lists from lists module: spellchecks to ignore and text replacements to make_____________________________
    global text_replacements    

    # Set criteria for ignoring a page__________________________________________________________________________________

    # Set variables, ignore_page, which is false by default, Becomes true if page is annex, glossary, etc
    # end_doc is triggered when the first words on a page indicate the procedure is finished with the doc (e.g. annex)
    ignore_page = False
    end_doc = False

    # Open the txtfile
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

    # match the case of the searchwords and the text file. Then see if any
    # searchwords exist in the text.____________________________________________________________________________________

    # Count the matches of the searchword patterns
    number_searchwords = 0

    for pattern in searchword_patterns:
        matches = pattern.findall(text)
        number_searchwords += len(matches)

    searchwords_present = number_searchwords > 0

    # Create the dictionary
    page_sentences = {}
    page_key = "Page " + str(page_num)
    for searchword in searchwords:
        page_sentences[searchword] = {page_key: []}

    # If none of the searchword patterns are present, return a dictionary with empty keys
    if not searchwords_present or ignore_page == True:
        return page_sentences, ignore_page, end_doc

    # Otherwise the remainder of code will run and extract sentences containing searchwords
    # Make conversions - lower case, temporarily removing stopwords, strippig hyphens___________________________________

    # Convert the text to lower case
    low_text = text.lower().strip()
    # low_text = re.sub(r"\([^)]*\)", "", low_text) # Strip out any terms in parenthesis

    # Remove punctutation that stops word boundary recognition
    for correction in text_replacements:
        low_text = low_text.replace(correction[0], correction[1])

    # Temporarily replace stopwords with placeholders
    stopwords_lower = [sw.lower() for sw in stop_words]
    placeholder_words = ["plhwd{0}".format(i) for i in range(len(stopwords_lower))]
    for i in range(len(stopwords_lower)):
        low_text = low_text.replace(stopwords_lower[i], placeholder_words[i])

    for searchword in searchwords:
        low_text = low_text.replace(searchword, searchword.upper())

    # # Make all searchwords in the text upper case to emphasise them in the resulting doc
    for searchword in searchwords:
        low_text = low_text.replace(searchword.lower(), searchword.upper())

    # Add searched sentences to the dictionary _________________________________________________________________________
    for i in range(len(searchwords)):
        matches = searchsentence_patterns[i].findall(low_text)
        for j in range(len(matches)):
            for k in range(len(placeholder_words)):
                matches[j] = matches[j].replace(
                    placeholder_words[k], stopwords_lower[k]
                )

        if len(matches) > 0:
            page_sentences[searchwords[i]][page_key] = matches

    return page_sentences, ignore_page, end_doc


def doc_search(
    dir_path, searchwords, searchword_patterns, searchsentence_patterns, stop_words=[]
):
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
        page_dictionary, ignore_page, end_doc = page_search(
            txtfile=txtfile,
            searchwords=searchwords,
            searchword_patterns=searchword_patterns,
            searchsentence_patterns=searchsentence_patterns,
            page_num=page_num,
            stop_words=stop_words,
        )

        # If the page was one that triggers a document -end event, finish the procedure and return the dictionary
        if end_doc == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ended procedure")
            return doc_sentences

        # If the page was one that should be ignored (annex, glossary), do not include it - move to next loop
        if ignore_page == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ignored")
            continue

        for searchword, value in page_dictionary.items():
            page_list = value[page_key]
            if len(page_list) != 0:
                doc_sentences[searchword][page_key] = page_list
                doc_sentences[searchword]["Total"] += len(page_list)

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
    subdir_list = subdir_list[::-1]

    # Create the document and write its title
    document = Document()
    p = document.add_paragraph("Searchword Results")
    p.style = document.styles["Title"]

    # Make regex patterns of searchwords for the doc and page search functions.
    # A list of patterns - just the words surrounded by word boundaries
    searchword_patterns = [
        re.compile(r"\b" + w + r"\b", re.IGNORECASE) for w in searchwords
    ]

    # a list of patterns - the sentences containing the words
    searchsentence_patterns = [
        re.compile(r"[^.]*\b" + w + r"\b[^.]*\.", re.IGNORECASE) for w in searchwords
    ]

    # For each txtfile folder, create a wordsearch dictionary, a header in the word doc
    # for the filename, subheaders for searchwords, and text for the sentences

    for subdir in subdir_list:
        total_searchwords_count = 0
        # print("\n", subdir)
        txtfile_dict = doc_search(
            dir_path=subdir,
            searchwords=searchwords,
            searchword_patterns=searchword_patterns,
            searchsentence_patterns=searchsentence_patterns,
            stop_words=stop_words,
        )
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
