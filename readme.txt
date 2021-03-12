Word Scraper Tool Instructions

Created by Lee Robinson

1. In a folder in the project directory, create a folder called PDF Files

2. Within that folder, create another folder with your project's name

3. In the Dashboard script, type in your project's name: project_name = "<your_project_name>"

Conversion____
4. Run the 'create_txt_files' function with the default arguments: create_txt_files(input_dir=pdf_dir, output_dir=txt_dir, results_dir=results_dir). This converts the PDFs to the txt files so they can be analysed

Analysis_____
5a. Specify the list of searchwords to count and stopwords to ignore (ignore sentences containing these, unless they also contain the searchwords). use regex in the searchwords if needed.

5b. Specify the 'Reported searchwords' list. These are the natural language versions of the regex terms in the searchwords list and are purely for cosmetic reasons - although they do need to be populated for the code to run. Ensure they are in the same order as your searchwords.

6. To get the Excel printout with wordcounts, run the entries_in_dir function with the default arguments
entries_in_dir(
    input_dir=txt_dir,
    results_dir=results_dir,
    searchwords=searchwords,
    stop_words=stop_words,
    project_name=project_name,
)

7. It can also produce a word doc that has all sentences containing your keywords - this is to allow deeper probing of whether particular uses of a search term count or not (which depends on your own analytical needs). 

Both the Excel and Word printouts will be created in the Results folder and will include a timestamp

There are also auxiliary functions that canbe modified
make_master_spelling_list produces a document with the spelling errors and their page numbers in each document 
text_fixer is used in spellchecking and analysis functions and can be modified to specify which text strings shoudl be replaced with which other ones. THis is very subject specific, so it is worth examining this function and its input iterators.


