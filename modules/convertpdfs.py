from wordscraper import *


def create_pdf_list(input_dir):
    # Makes a list of the filenames + extensions for all files in a directory
    # Reverses it so the files with most recent years in their titles appear first

    filenames = [f for f in listdir(input_dir) if isfile(join(input_dir, f))]
    filenames.reverse()  # To analyse the latest reports first
    return filenames


class StopExecution(Exception):
    def _render_traceback_(self):
        pass


def convert_pdfminer(filename, input_dir, output_dir, password="", cleancycles=10):
    # Converts a pdf into several text files, in a directory named after the
    # pdf file. Also cleans up whitespace and carriage returns

    proc_time_start = process_time()

    input_filepath = os.path.join(input_dir + filename)
    filename = filename.replace(input_dir, "").replace(".pdf", "")
    allfiles_output_dir = output_dir
    thisfile_output_dir = allfiles_output_dir + "\\" + filename + "\\"

    # Create the parent 'txt_converts' directory
    try:
        if not os.path.exists(allfiles_output_dir):
            os.makedirs(allfiles_output_dir)
    except OSError:
        print("Error: Creating directory. " + thisfile_output_dir)

    # # Remove old version of the individual pdf directory
    try:
        if os.path.exists(thisfile_output_dir):
            shutil.rmtree(thisfile_output_dir)
    except OSError:
        print("Error: Creating directory. " + thisfile_output_dir)

    # Create the new individual pdf directory
    try:
        os.makedirs(thisfile_output_dir)
    except OSError:
        print("Error: Creating directory. " + thisfile_output_dir)

    # Open and read the pdf file in binary mode
    fp = open(input_filepath, "rb")

    # Create parser object to parse the pdf content
    parser = PDFParser(fp)

    # Store the parsed content in PDFDocument object
    document = PDFDocument(parser, password)

    # Check if document is extractable, if not abort
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create PDFResourceManager object that stores shared resources such as fonts or images
    rsrcmgr = PDFResourceManager()

    # set parameters for analysis
    laparams = LAParams()

    # Create a PDFDevice object which translates interpreted information into desired format
    # Device needs to be connected to resource manager to store shared resources
    # device = PDFDevice(rsrcmgr)
    # Extract the decive to page aggregator to get LT object elements
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create interpreter object to process page content from PDFDocument
    # Interpreter needs to be connected to resource manager for shared resources and device
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Ok now that we have everything to process a pdf document, lets process it page by page
    iter = 0
    for page in PDFPage.create_pages(document):
        extracted_text = ""

        # As the interpreter processes the page stored in PDFDocument object
        interpreter.process_page(page)
        # The device renders the layout from interpreter
        layout = device.get_result()
        # Out of the many LT objects within layout, we are interested in LTTextBox and LTTextLine
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                extracted_text += lt_obj.get_text()

        # Clean Up the text: remove carriage returns
        extracted_text = extracted_text.replace(" \n", " ")
        extracted_text = extracted_text.replace("\n", "")
        j = 1
        while j < cleancycles:  # Remove whitespace
            extracted_text = extracted_text.replace("  ", " ")
            j += 1

        if iter < 9:
            txtfile_num = "0" + str(iter + 1)
        else:
            txtfile_num = str(iter + 1)

        log_file = thisfile_output_dir + "page_" + txtfile_num + ".txt"
        # Delete old versions
        # if os.path.exists(log_file):
        #     os.remove(log_file)

        with open(log_file, "wb") as my_log:
            my_log.write(extracted_text.encode("utf-8"))

        iter += 1

        proc_time_end = process_time()

    proc_time_total = proc_time_end - proc_time_start
    return proc_time_total


def create_txt_files(input_dir, output_dir, results_dir, password="", cleancycles=10):
    # Applies the convert_pdfminer to all pdfs in a directory, and produces a
    # dictionary with the time each one took to convert and the total time

    # Set the timer to time the process
    total_time_start = process_time()

    # Create a list of the files to convert and their filenamaes without extensions
    pdf_list = create_pdf_list(input_dir)
    pdf_names = [pdf.replace(".pdf", "") for pdf in pdf_list]

    # Create the Excel file and initialise header values
    timefile = results_dir + "PDF Processing Times.xlsx"
    if not os.path.exists(timefile):
        wb = Workbook()
        ws = wb.active
        ws.title = "Times"
    else:
        wb = load_workbook(timefile)
        ws = wb["Times"]

    ws["A1"] = "File"
    ws["B1"] = "Time"

    # Create a dictionary to keep track of time to convert each pdf and total time
    time_dict = dict.fromkeys(pdf_names)

    # Convert each pdf, keeping track of the time each takes in the dictionary
    row = int(len(ws["A"]))
    if row == 1:
        row = 2

    done_pdfs = []

    for iter_row in ws.iter_rows(min_row=2, max_col=1, max_row=row):
        for cell in iter_row:
            done_pdfs.append(cell.value)

    for pdf in pdf_list:
        pdf_name = pdf_names[pdf_list.index(pdf)]
        if pdf_name in done_pdfs:
            continue
        # row += 1
        ws["A" + str(row)] = pdf_name
        try:
            pdf_time = convert_pdfminer(
                filename=pdf,
                input_dir=input_dir,
                output_dir=output_dir,
                password=password,
                cleancycles=cleancycles,
            )
        except:
            print(pdf_name + " not processed")
            continue
        time_dict[pdf_name] = pdf_time
        ws["B" + str(row)] = pdf_time
        wb.save(results_dir + "Processing Times.xlsx")
        row += 1
        print("Done " + pdf_name + ", Time: " + str(pdf_time))

    # # Record the total time
    total_time_end = process_time()
    time_dict["Total"] = total_time_end - total_time_start

    print(
        "PDFs converted to txt files. Processing Times reported in Processing Times.xlsx in results folder"
    )
    return time_dict


def undone_converts(input_dir, results_dir):
    # Of all pdfs in the input directory, generates a list of those not yet
    # processed into txt files. Useful to run after converting PDFs to see which ones failed

    wb = load_workbook(results_dir + "Processing Times.xlsx")
    ws = wb["Times"]
    row = int(len(ws["A"]))

    pdf_list = create_pdf_list(input_dir)
    pdf_names = [pdf.replace(".pdf", "") for pdf in pdf_list]

    done_pdfs = []
    for iter_row in ws.iter_rows(min_row=2, max_col=1, max_row=row):
        for cell in iter_row:
            done_pdfs.append(cell.value)

    undone_converts = []
    for pdf in pdf_names:
        if pdf not in done_pdfs:
            undone_converts.append(pdf)

    return undone_converts
