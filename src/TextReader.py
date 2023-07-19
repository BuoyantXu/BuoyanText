from functools import partial
from multiprocessing import Pool
import os
import re
import pandas as pd
import fitz


def file_list_reader(file_paths=None, save_text=True, name_pattern="", normalizer=None, threading=1):
    f_reader = partial(file_reader, save_text=save_text, name_pattern=name_pattern, normalizer=normalizer)
    if threading > 1:
        with Pool(threading) as p:
            rows = p.map(f_reader, file_paths)
    else:
        rows = [f_reader(fp) for fp in file_paths]

    data = pd.DataFrame(rows)

    return data


def file_reader(fp=None, save_text=True, name_pattern="", normalizer=None):
    name = os.path.basename(fp)
    file_type = name.split(".")[-1]
    name = name.split(".")[0]
    error_file, error_text, error_name = (0, 0, 0)

    # (1) name pattern
    if name_pattern:
        name, error_name = check_name_error(name=name, name_pattern=name_pattern)

    # (2) file error and text error
    text, (error_file, error_text) = check_text(
        fp=fp, file_type=file_type, save_text=save_text, normalizer=normalizer)

    row = {
        "file_path": fp, "name": name, "error_file": error_file, "error_name": error_name
    }
    if save_text:
        row["error_text"] = error_text
        row["text"] = text

    return row


def check_text(fp, file_type="pdf", save_text=True, normalizer=None):
    # pdf
    text = ""
    error_file = 0
    error_text = 0
    if file_type == "pdf":
        try:
            with fitz.open(fp) as doc:
                if save_text:
                    text = "".join([page.get_text() for page in doc])
                    error_text = check_text_error(text)
                    if (normalizer is not None) & (not error_text):
                        normalizer.text = text
                        text = normalizer.normalize()
        except Exception as e:
            print(f"{e}: {fp}")
            error_file = 1
    # txt
    elif file_type == "txt":
        try:
            with open(fp, "r") as doc:
                if save_text:
                    text = doc.readlines()
                    error_text = check_text_error(text)
                    if (normalizer is not None) & (not error_text):
                        normalizer.text = text
                        text = normalizer.normalize()
        except Exception as e:
            print(f"{e}: {fp}")
            error_file = 1

    return text, (error_file, error_text)


def check_text_error(text):
    error_text = 1 if text.count("�") / (len(text) + 1) > 0.4 else 0

    return error_text


def check_name_error(name, name_pattern):
    if r := re.findall(pattern=name_pattern, string=name):
        name = r[0]
        error_name = 0
    else:
        error_name = 1

    return name, error_name


def pdf_to_txt(fp, path_to=""):
    name = os.path.basename(fp).split(".")[0]
    file_type = fp.split(".")[-1]

    if file_type == "pdf":
        with fitz.open(fp) as doc:
            text = "".join([page.get_text() for page in doc])
        # save to txt
        with open(os.path.join(path_to, name + ".txt"), "w", encoding="UTF-8") as f:
            f.write(text)
    else:
        print(f"file type error: {fp}")

    return text
