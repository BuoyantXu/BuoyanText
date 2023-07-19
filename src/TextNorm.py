import re
import json
import unicodedata
from bs4 import BeautifulSoup
import spacy
import jieba
import nltk
from nltk.corpus import wordnet
from nltk.tokenize.toktok import ToktokTokenizer


tokenizer = ToktokTokenizer()
spacy_nlp = spacy.load('en_core_web_sm')

# English
with open('nlp_data/English/stopwords.json', 'r') as f:
    stopwords_English = json.load(f)
with open('nlp_data/English/contractions.json', 'r') as f:
    contractions = json.load(f)
# Chinese
with open('nlp_data/Chinese/stopwords.json', 'r') as f:
    stopwords_Chinese = json.load(f)
with open('nlp_data/Chinese/punctuation.json') as f:
    punctuation = json.load(f)


class TextNorm:
    text = ""
    normalized_text = None

    def __init__(self, text="", language="English",
                 # Uniform
                 html_stripping=True, remove_repeated=False, remove_digits=True, stopwords_removal=True,
                 special_char_removal=True,
                 # English
                 contraction_expansion=True, accented_char_removal=True, text_lower_case=True, text_stemming=False,
                 text_lemmatization=True,
                 # Chinese
                 split_words=True, punctuation_drop=True):

        self.text = text
        self.normalized_text = None

        # English
        if language in ["English", "english", "eng", "ENG", "en", "英文"]:
            self.language = "English"
            self.stopwords = stopwords_Chinese
            self.contractions = contractions

            self.option = {
                # Uniform approach
                "html_stripping": html_stripping, "remove_repeated": remove_repeated, "remove_digits": remove_digits,
                "stopwords_removal": stopwords_removal, "special_char_removal": special_char_removal,

                # English
                "contraction_expansion": contraction_expansion, "accented_char_removal": accented_char_removal,
                "text_lower_case": text_lower_case, "text_stemming": text_stemming,
                "text_lemmatization": text_lemmatization
            }

        # Chinese
        elif language in ["Chinese", "chinese", "chi", "CHI", "cn", "中文"]:
            self.language = "Chinese"
            self.stopwords = stopwords_Chinese
            self.punctuation = punctuation

            self.option = {
                # Uniform approach
                "html_stripping": html_stripping, "remove_repeated": remove_repeated, "remove_digits": remove_digits,
                "stopwords_removal": stopwords_removal, "special_char_removal": special_char_removal,

                # Chinese
                "split_words": split_words, "punctuation_drop": punctuation_drop
            }
        else:
            raise "Language setting error! Only support English and Chinese for now."

    def normalize(self):
        text = self.text
        option = self.option
        language = self.language

        text = normalize_uniform(text, option, language)
        if language == "English":
            text = normalize_en(text, option)
        elif language == "Chinese":
            text = normalize_cn(text, option)

        self.normalized_text = text
        return text


# Uniform approach
def normalize_uniform(text, option, language="English"):
    # (1) strip html tags
    if option['html_stripping']:
        text = strip_html_tags(text)

    # (2) remove repeated words
    if option['remove_repeated']:
        text = remove_repeated_characters(text)

    # (3) remove digits
    if option['remove_digits']:
        text = remove_numbers(text)

    # (4) remove stopwords
    if option['stopwords_removal']:
        text = remove_stopwords(text)

    # (5) special char removal
    if option['special_char_removal']:
        text = remove_special_characters(text, language=language)

    return text


# English
def normalize_en(text, option):
    # (1) contractions
    if option['contraction_expansion']:
        text = expand_contractions(text, contraction_mapping=contractions)

    # (2) accented char removal
    if option['accented_char_removal']:
        text = remove_accented_chars(text)

    # (3) text lower case
    if option['text_lower_case']:
        text = text.lower()

    # (4) text stemming
    if option['text_stemming']:
        text = simple_porter_stemming(text)

    # (5) text lemmatization
    if option['text_lemmatization']:
        text = lemmatize_text(text, nlp=spacy_nlp)

    return text


# Chinese
def normalize_cn(text, option):
    # (1) split words (分词)
    if option['split_words']:
        text = words_split(text)

    # (2) drop punctuation
    if option['punctuation_drop']:
        text = drop_punctuation(text)

    return text


# (1) Uniform approach
def strip_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    if bool(soup.find()):
        [s.extract() for s in soup(['iframe', 'script'])]
        stripped_text = soup.get_text()
        stripped_text = re.sub(r'[\r|\n]+', '\n', stripped_text)
    else:
        stripped_text = text

    return stripped_text


def remove_repeated_characters(tokens):
    repeat_pattern = re.compile(r'(\w*)(\w)\2(\w*)')
    match_substitution = r'\1\2\3'

    def replace(old_word):
        if wordnet.synsets(old_word):
            return old_word
        new_word = repeat_pattern.sub(match_substitution, old_word)
        return replace(new_word) if new_word != old_word else new_word

    correct_tokens = [replace(word) for word in tokens]

    return correct_tokens


def remove_numbers(doc):
    return re.sub(r'\d+', '', doc)


def remove_stopwords(text, is_lower_case=False, language="English"):
    if language == "English":
        stopwords = stopwords_English
        tokens = tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        if is_lower_case:
            filtered_tokens = [token for token in tokens if token not in stopwords]
        else:
            filtered_tokens = [token for token in tokens if token.lower() not in stopwords]
        text = ' '.join(filtered_tokens)
    elif language == "Chinese":
        stopwords = stopwords_Chinese
        text = [word for word in text.split() if word not in stopwords]

    return text


def remove_special_characters(text, language="English"):
    if language == "English":
        pattern = r'[^a-zA-Z0-9\s]|\[|\]'
        text = re.sub(pattern, '', text)
    elif language == "Chinese":
        text = re.findall(
            '[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa50-9]',
            text)
        text = "".join(text)

    return text


# (2) English text
def expand_contractions(text, contraction_mapping=None):
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())),
                                      flags=re.IGNORECASE | re.DOTALL)

    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match) \
            if contraction_mapping.get(match) \
            else contraction_mapping.get(match.lower())
        expanded_contraction = first_char + expanded_contraction[1:]
        return expanded_contraction

    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)

    return expanded_text


def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    return text


def simple_porter_stemming(text):
    ps = nltk.porter.PorterStemmer()
    text = ' '.join([ps.stem(word) for word in text.split()])

    return text


def lemmatize_text(text, nlp=None):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])

    return text


# (3) Chinese text
def words_split(text):
    text = jieba.cut(text, use_paddle=True)
    text = [s for s in text if s not in stopwords_Chinese]
    text = " ".join(text)

    return text


def drop_punctuation(text):
    text = re.sub(r"[{}]+".format(punctuation), "", text)
    text = re.sub(r"\s+", " ", text)

    return text
