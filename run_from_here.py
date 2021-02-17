from wordscraper import *

project_name = "UNGA and G20"

project_dir, pdf_dir, txt_dir, results_dir = directories(project_name)

global searchwords
global stop_words

# create_txt_files(input_dir=pdf_dir, output_dir=txt_dir, results_dir=results_dir)
txt_dir = "C:\\Users\\Lee\\Documents\\Python\\Projects\\Tools\\Word Scraper\\TXT Files\\UNGA and G20\\"

txtfile = "C:\\Users\\Lee\\Documents\\Python\\Projects\\Tools\\Word Scraper\\TXT Files\\Test Project\\G20 2019 Leaders Declaration\\page_01.txt"

dir_spellcheck(input_dir=txt_dir, results_dir=results_dir)

# misspelled, ignore_page, end_doc = page_spellcheck(txtfile)
# print(misspelled)

# page_spellcheck(txtfile)

# print(spellcheck_ignore)

# write_doc(
#     input_dir=txt_dir,
#     results_dir=results_dir,
#     searchwords=searchwords,
#     # stop_words=stop_words,
#     project_name=project_name,
# )

# entries_in_dir(
#     input_dir=txt_dir,
#     results_dir=results_dir,
#     searchwords=searchwords,
#     stop_words=stop_words,
#     project_name=project_name,
# )
