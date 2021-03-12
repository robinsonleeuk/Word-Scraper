from wordscraper import *

project_name = "UNGA"

project_dir, pdf_dir, txt_dir, results_dir = directories(project_name)


searchwords = [
    r"Environment[a-zA-Z*]",  # to capture environmental,
    "Climate",
    "Weather",
    r"Destabili[sz]ation",
    "Sea level",
    "Ozone",
    "ETS",
    r"Renewable[s]*",
    "sequestration",
    r"emission[s*]",
]

reported_searchwords = [
    "Climate",
    "Destabilisation",
    "Emission",
    "Environment",
    "ETS",
    "Ozone",
    "Renewables",
    "Sea Level",
    "Sequestration",
    "Weather",
]

stop_words = [
    "Business Climate",
    "Political Climate",
    "Investment Climate",
    "Transparent Climate",
    "Business Environment",
    "Political Environment",
    "Transparent Environment",
    "Investment Environment",
]

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
