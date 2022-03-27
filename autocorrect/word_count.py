import json
import re
from collections import Counter, OrderedDict

from autocorrect.constants import word_regexes


def get_words(filename, lang, encd, from_first=False):
    word_regex = word_regexes[lang]
    if from_first:
        capitalized_regex = r'(\.|^|<|"|\'|\(|\[|\{)\s*'
    else:
        capitalized_regex = r'(\.|^|<|"|\'|\(|\[|\{)\s*' + word_regexes[lang]
    with open(filename, encoding=encd) as file:
        for line in file:
            line = re.sub(capitalized_regex, "", line)
            yield from re.findall(word_regex, line)


def count_words(src_filename, lang, encd="utf-8", out_filename="word_count.json", from_first=False):
    words = get_words(src_filename, lang, encd, from_first=from_first)
    counts = Counter(words)
    # make output file human readable
    counts_list = list(counts.items())
    counts_list.sort(key=lambda i: i[1], reverse=True)
    counts_ord_dict = OrderedDict(counts_list)
    with open(out_filename, "w") as outfile:
        json.dump(counts_ord_dict, outfile, indent=4)
