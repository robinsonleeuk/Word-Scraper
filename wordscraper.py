# Import various modules to store the results in dataframes and time the procedure
import os
import pathlib
import re
import shutil
from datetime import datetime
from os import listdir
from os.path import isfile, join
from time import process_time

import docx
import pandas as pd
from docx import Document
from docx.text.paragraph import Paragraph
from openpyxl import load_workbook
from openpyxl.styles import (
    Alignment,
    Border,
    Color,
    Font,
    GradientFill,
    NamedStyle,
    PatternFill,
    Side,
    colors,
)
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook import Workbook
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from spellchecker import SpellChecker

from modules.convertpdfs import *
from modules.directories import *
from modules.extractsentences import *
from modules.functions import *
from modules.spellcheck import *
from modules.wordcounter import *
