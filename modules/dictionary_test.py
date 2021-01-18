import pandas as pd

# extract_sentences = {
#     "Climate": {
#         "Total": 20,
#         "Page 1": [
#             "First climate Entry",
#             "Second climate Entry",
#             "Third Environment Entry",
#         ],
#         "Total": 20,
#         "Page 2": [
#             "First climate Entry",
#             "Second climate Entry",
#             "Third climate Entry",
#         ],
#     },
#     "Environment": {
#         "Total": 20,
#         "Page 1": [
#             "First Environment Entry",
#             "Second Environment Entry",
#             "Third Environment Entry",
#         ],
#         "Total": 20,
#         "Page 2": [
#             "First Environment Entry",
#             "Second Environment Entry",
#             "Third Environment Entry",
#         ],
#     },
# }


word_count = {
    "Document": [
        "Doc1",
        "Doc2",
        "Doc3",
        "Doc4",
    ],
    "Pages": [
        "Doc1 Pages",
        "Doc2 Pages",
        "Doc3 Pages",
        "Doc4 Pages",
    ],
    "Searchword1": [
        "Doc1 Searchword1",
        "Doc2 Searchword1",
        "Doc3 Searchword1",
        "Doc4 Searchword1",
    ],
    "searchword2": [
        "Doc1 searchword2",
        "Doc2 searchword2",
        "Doc3 searchword2",
        "Doc4 searchword2",
    ],
    "searchword3": [
        "Doc1 searchword3",
        "Doc2 searchword3",
        "Doc3 searchword3",
        "Doc4 searchword3",
    ],
    "searchword4": [
        "Doc1 searchword4",
        "Doc2 searchword4",
        "Doc3 searchword4",
        "Doc4 searchword4",
    ],
}

df = pd.DataFrame.from_dict(word_count)
print(df)
