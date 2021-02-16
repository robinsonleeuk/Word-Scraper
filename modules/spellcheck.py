from wordscraper import *


def page_spellcheck(txtfile):
    # Opens a txt file and searches it for misspelled words

    ignore_page = False
    end_doc = False

    misspelled = []

    # Open the txtfile
    try:
        text = open(txtfile, "r", encoding="utf8").read()
    except:
        text = open(txtfile, "r", encoding="ISO-8859-1").read()

    # Make the text lower case for fewer case conflicts
    low_text = text.lower()

    # Strip out hyphens
    low_text = low_text.replace("-", " ").replace("–", "")

    # Take first hundred words to check for ignore or stop criteria
    first_hundred_list = low_text.split()[0:100]
    first_hundred_string = " ".join(first_hundred_list)

    # check if they contain 'Annex' and end docuemnt search if so
    annex_pattern = re.compile(r"^annex[:]*", re.IGNORECASE)
    annex_match = re.search(annex_pattern, first_hundred_string)

    if annex_match:
        ignore_page = True
        end_doc = True

    # Check if they are table of contents and ignore page if so
    contents_pattern = re.compile(r"^contents", re.IGNORECASE)
    contents_match = re.search(contents_pattern, first_hundred_string)

    if contents_match:
        ignore_page = True

    # If none of the searchword patterns are present, return an empty list
    if ignore_page == True:
        # if not searchwords_present or ignore_page == True:
        return misspelled, ignore_page, end_doc

    # Otherwise the remainder of code will run and extract sentences containing misspelled words

    # Extract a list of potentially misspelled words____________________________________________________________________
    spell = SpellChecker()

    text_list = low_text.split()
    for i in range(len(text_list)):
        text_list[i] = (
            text_list[i]
            .replace(",", "")
            .replace(".", "")
            .replace(";", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", " ")
            .replace("–", "")
            .replace("'s", "s")
        )

    misspelled = spell.unknown(text_list)

    return misspelled, ignore_page, end_doc


def doc_spellcheck(dir_path):
    # Searches for the misspelled words in all of the txt files in a given directory. Returns dictionary with the page numbers as keys,
    # and lists of unregonised words as the values

    # Create lists: txtfiles to read, page numbers, and pagenum keys for dictionary
    filenames = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    page_nums = [f.replace(".txt", "").replace("page_", "") for f in filenames]
    page_keys = ["Page " + pn for pn in page_nums]

    # Initialize the dictionary that will store results, with 0 totals of each word
    misspelled_dict = {}

    # Iterate through the txtfiles in the dir by pagenumber creating wordcount dictionaries
    # for that page then adding results to the parent document dictionary
    for page_num in page_nums:
        txtfile = dir_path + filenames[page_nums.index(page_num)]
        page_key = page_keys[page_nums.index(page_num)]
        misspelled_words, ignore_page, end_doc = page_spellcheck(txtfile)

        # If the page was one that triggers a document -end event, finish the procedure and return the dictionary
        if end_doc == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ended procedure")
            return misspelled_dict

        # If the page was one that should be ignored (annex, glossary), do not include it - move to next loop
        if ignore_page == True:
            # print("page_", end="")
            # print(page_num, end="")
            # print(" ignored")
            misspelled_words = []

        if len(misspelled_words) != 0:
            misspelled_dict[page_key] = misspelled_words

    # Create a list of searchwords with no results
    keys_to_delete = []
    for page_key in page_keys:
        if len(misspelled_dict[page_key]) == 0:
            keys_to_delete.append(page_key)

    # Delete the searchwords with no results from the dictionary
    for key in keys_to_delete:
        del misspelled_dict[key]

    return misspelled_dict


def delete_paragraph(paragraph):
    # Deletes paragraphs using docx

    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None


def dir_spellcheck(input_dir, results_dir):
    # Writes the sentences containing keywords to an existing a word document
    # with a Level 1 header for the doc name, Level 2 for each searchword
    # and level 3 for each page that has sentences containing it

    # Construct the string for the filename + time and its filepath
    now = datetime.now()
    dt_string = now.strftime("%Y%m%d_%H%M")
    project_filename = "Spelling Errors_" + dt_string + ".docx"
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
    p = document.add_paragraph("Spellcheck Results")
    p.style = document.styles["Title"]

    for subdir in subdir_list:
        misspelled_dict = doc_spellcheck(dir_path=subdir)
        filename = filename_list[subdir_list.index(subdir)]
        filename_para = document.add_paragraph(filename)
        filename_para.style = document.styles["Heading 1"]

        # Report the search results
        for page_key, results in misspelled_dict.items():
            searchword_header = page_key
            p = document.add_paragraph(searchword_header)
            p.style = document.styles["Heading 2"]

            mispelled_word_para = ", ".join(results)
            try:
                p = document.add_paragraph(mispelled_word_para)
            except:
                p = document.add_paragraph(
                    "<<Unable to add this paragraph - format conversion error>>"
                )
            p.style = document.styles["Normal"]

    document.save(filepath)
    print("Sentences Extracted to " + project_filename + " in results folder")
