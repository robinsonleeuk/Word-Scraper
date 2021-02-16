from wordscraper import *

project_name = "UNGA and G20"

project_dir, pdf_dir, txt_dir, results_dir = directories(project_name)

searchwords = [
    "Global warming",
    "Environment",
    "Climate",
    "Carbon",
    "Carbon pricing",
    "Carbon price",
    "Man Made",
    "Man-Made",
    "Anthropogenic",
    "Weather",
    "Destabilisation",
    "Destabilization",
    "Extreme events",
    "Environmental destruction",
    "Sea level",
    "Greenhouse",
    "Ozone",
    "CO2",
    "ETS",
    "Emissions Trading System",
    "Renewable",
    "Solar Power",
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

# write_doc(
#     input_dir=txt_dir,
#     results_dir=results_dir,
#     searchwords=searchwords,
#     stop_words=stop_words,
#     project_name=project_name,
# )

# entries_in_dir(
#     input_dir=txt_dir,
#     results_dir=results_dir,
#     searchwords=searchwords,
#     stop_words=stop_words,
#     project_name=project_name,
# )
