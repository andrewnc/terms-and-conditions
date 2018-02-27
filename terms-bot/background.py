import json
import re

from flask import Flask, request, render_template
from flask_cors import CORS
from preprocessing import prepare_for_regex
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer

import unidecode

# file structure for display, will update
HTML_OPEN = "<div id='mainPopup'>"
YOU_AGREE_HEADER = "<div id='youAgree' class='header'>What You Agree</div>"
THEY_AGREE_HEADER = "<div id='theyAgree' class='header'>What They Agree</div>"
OTHER_HEADER = "<div id='other' class='header'>Other Clauses</div>"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def serve_homepage():
    return render_template("Legal Leaf.htm")


@app.route('/background.py', methods=['POST', 'GET', 'OPTIONS'])
def index():
    # globals
    LANGUAGE = 'english'
    SENTENCES_COUNT = 10
    clause = re.compile("(will)|(agree)|(must)|(responsib)|(waive)|(lawsuit)|(modify)|(intellec)")

    # extract data from the extension
    req = request.form
    text_data = " ".join(list(req.keys()))

    text_data = unidecode.unidecode(text_data)
    clean_list, pure_list = prepare_for_regex(text_data)

    data_to_summarize = []
    for clean, pure in zip(clean_list, pure_list):
        if re.findall(clause, clean):
            data_to_summarize.append(pure)

    text_data = " ".join(data_to_summarize)
    # create parsers and summarize
    parser = PlaintextParser(text_data, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = KLSummarizer(stemmer)

    # get summary
    summary = summarizer(parser.document, SENTENCES_COUNT)

    # return the summary sentences
    sentences = [str(x) for x in summary]
    message = HTML_OPEN + "<ul class='rolldown-list' id='myList'>"

    you_agree = []
    they_agree = []
    other_clause = []
    for sentence in sentences:
        # TODO: logging in the future
        lower = sentence.lower()
        you_idx = lower.find("you")
        they_idx = lower.find("we")
        if (you_idx == -1 or you_idx > 15) and (they_idx == -1 or they_idx > 15):
            other_clause.append(sentence)
        elif you_idx == -1:
            they_agree.append(sentence)
        elif they_idx == -1:
            you_agree.append(sentence)
        elif you_idx < they_idx:
            you_agree.append(sentence)
        else:
            they_agree.append(sentence)

    if len(you_agree) > 0:
        message += YOU_AGREE_HEADER + "<li>"
        message += "</li><li>".join(you_agree)
        message += "</li>"

    if len(they_agree) > 0:
        message += THEY_AGREE_HEADER + "<li>"
        message += "</li><li>".join(they_agree)
        message += "</li>"

    if len(other_clause) > 0:
        message += OTHER_HEADER + "<li>"
        message += "</li><li>".join(other_clause)
        message += "</li>"

    message += "</ul></div>"

    # sends response back to the extension
    return json.dumps(message)


if __name__ == "__main__":
    app.run()
