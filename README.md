# BuoyanText
### v0.0.5 20230720
___
## TextNorm.py

**TextNorm** class

Normalizing English or Chinese text

**Arguments:**

    text="", language="English",
    # Uniform
    html_stripping=True, remove_repeated=False, remove_digits=True, stopwords_removal=True,
    special_char_removal=True, 
    # English
    contraction_expansion=True, accented_char_removal=True, text_lower_case=True, text_stemming=False, 
    text_lemmatization=True, 
    # Chinese
    split_words=True, punctuation_drop=True

- text: the text need to be normalized
- language: "English" or "Chinese" (default: "English")

(1) Uniform approach arguments

- html_stripping:       strip html tags if True (default: True)
- remove_repeated:      remove repeated words (default: False)
- remove_digits:        remove numbers (default: True)
- stopwords_removal:    remove stopwords (default: True)
- special_char_removal: remove special characters (default: True)

(2) English text arguments

- contraction_expansion: expand contractions, for example "can't" to "can not" (default: True)
- accented_char_removal: (default: True)
- text_lower_case:       (default: True)
- text_stemming:         (default: False)
- text_lemmatization:    (default: True)

(3) Chinese text arguments

- split_words:      split words with jieba (default: True)
- punctuation_drop: drop punctuations (default: True)

___
## TextReader.py

**(1) file_reader**

**(2) file_list_reader**

**(3) pdf_to_txt**
