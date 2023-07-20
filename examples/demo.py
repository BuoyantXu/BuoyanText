from BuoyanText.TextReader import file_list_reader, file_reader, pdf_to_txt
from BuoyanText.TextNorm import TextNorm


if __name__ == '__main__':
    file_paths = [
        "examples/data/000001平安银行2012年年度报告.pdf",
        "examples/data/000001平安银行2013年年度报告.pdf"
    ]

    ######################
    # TextReader example #
    ######################

    # (1) read single report pdf file
    check = file_reader(fp=file_paths[0])
    print(check.keys())

    # (2) read a list of reports
    check_list = file_list_reader(file_paths=file_paths)
    print(check_list)

    # (3) name pattern match
    check_names = file_list_reader(file_paths=file_paths, name_pattern="[0-9]{6}.+20[0-9]{2}")
    print(check_names)

    # (4) multiprocessing
    check_mult = file_list_reader(file_paths=file_paths, threading=2)
    print(check_mult)

    # (5) transform pdf file to txt
    pdf_to_txt(file_paths[0], path_to="examples")

    ####################
    # TextNorm example #
    ####################

    # text normalize
    tn = TextNorm(text=check['text'], language="cn")
    normalized_text = tn.normalize()
    print(tn.normalized_text)

    #########################
    # TextReader & TextNorm #
    #########################

    data = file_list_reader(file_paths=file_paths, normalizer=tn, threading=2)
    print(data.text[0])
