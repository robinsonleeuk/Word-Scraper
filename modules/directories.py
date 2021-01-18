import inspect
import os


def directories(project_name):
    project_dir = os.path.abspath(os.getcwd()) + "\\"
    pdf_dir = project_dir + "PDF Files\\" + project_name + "\\"
    txt_dir = project_dir + "TXT Files\\" + project_name + "\\"
    results_dir = project_dir + "Results\\" + project_name + "\\"
    for new_dir in [txt_dir, results_dir]:
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    return project_dir, pdf_dir, txt_dir, results_dir
