from wordscraper import *

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

spellcheck_ignore = [
    "g20",
    "aftermath",
    "gdp",
    "accommodative",
    "sdgs",
    "12th",
    "gfsec",
    "interoperability",
    "tsukuba",
    "epg",
    "oecd",
    "15th",
    "wbg",
    "g20s",
    "msmes",
    "concessional",
    "fsbs",
    "fatf",
    "epgs",
    "fsb",
    "beps",
    "fatfs",
    "macroprudential",
    "synergies",
    "employability",
    "matsuyama",
    "ilo",
    "ict",
    "cwa",
    "“no",
    "upscaling",
    "uhc",
    "19th",
    "roadmaps",
    "amr",
    "ipcc",
    "ipbes",
    "r&d",
    "talanoa",
    "194%",
    "irreversibility",
    "unfccc",
    "14%",
    "co2",
    "karuizawa",
    "ndcs",
    "recycling”",
    "ghg",
    "presidencys",
    "undisrupted",
    "iuu",
    "ccus",
    "value”",
    "microplastics",
    "iom",
    "unhcr",
    "distributional",
    "decision‐making",
    "antalya",
    "formalization",
    "reskilling",
    "25%",
    "icts",
    "competences",
    "pedagogies",
    "6°",
    "ecd",
    "cop24",
    "conditionality",
    "klaas",
    "finalization",
    "lics",
    "mr",
    "k",
    "intermediation",
    "communiqués",
    "iwg",
    "dwg",
    "fwg",
    "ifawg",
    "communiqué",
    "recognizant",
    "acwg",
    "sfsg",
    "gpfi",
    "cswg",
]

text_replacements = [
    ("-", " "),
    (":", " :"),
    ("´", ""),
    ("“", ""),
    ("/", " / "),
    ("‘", ""),
    ("%", " %"),
    ("’", ""),
    ("‐", " "),
]
