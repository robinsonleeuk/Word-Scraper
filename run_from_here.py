from wordscraper import *

project_name = "UNGA and G20"

project_dir, pdf_dir, txt_dir, results_dir = directories(project_name)

searchwords = [
    "Global warming",
    r"Environment[a-zA-Z*]",  # to capture environmental,
    "Climate",
    "Carbon",
    r"Carbon pric[a-zA-Z*]",  # pricing, prices, price
    "Man Made",
    "Anthropogenic",
    "Weather",
    r"Destabili[sz]ation",
    "Extreme events",
    "Sea level",
    "Greenhouse",
    "Ozone",
    "CO2",
    "ETS",
    r"Emissions Trading System[s]*",
    r"Emissions Trading scheme[s]*",
    r"Renewable[s]*",
    "Solar Power",
    "sequestration",
    r"emission[s*]",
    "climate finance",
    r"carbon tax[a-zA-Z*]",  # tax, taxes, taxing
    r"border tax[a-zA-Z*]",
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

# create_txt_files(input_dir=pdf_dir, output_dir=txt_dir, results_dir=results_dir)


dir_spellcheck(input_dir=txt_dir, results_dir=results_dir)

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
