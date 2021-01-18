from wordscraper import *

project_name = "Test Project"

project_dir, pdf_dir, txt_dir, results_dir = directories(project_name)

searchwords = ["Searchword 0", "Searchword 1"]

stop_words = ["Stopword 1", "Stopword 2"]

create_txt_files(input_dir=pdf_dir, output_dir=txt_dir, results_dir=results_dir)

write_doc(
    input_dir=txt_dir,
    results_dir=results_dir,
    searchwords=searchwords,
    stop_words=stop_words,
    project_name=project_name,
)

entries_in_dir(
    input_dir=txt_dir,
    results_dir=results_dir,
    searchwords=searchwords,
    stop_words=stop_words,
    project_name=project_name,
)
