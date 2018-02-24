import json
import re

from flask import Flask, request
from flask_cors import CORS
from preprocessing import prepare_for_regex
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer

# file structure for display, will update
HTML_OPEN = "<div id=\"mainPopup\"><h1>Welcome to legal summary bot</h1>"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/background.py', methods=['POST', 'GET', 'OPTIONS'])
def index():
    # globals
    LANGUAGE = 'english'
    SENTENCES_COUNT = 10
    clause = re.compile("(will)|(agree)|(must)|(responsib)|(waive)|(lawsuit)|(modify)|(intellec)")

    # extract data from the extension
    req = request.form
    text_data = " ".join(list(req.keys()))

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
    message = HTML_OPEN + "<ol>"

    for sentence in sentences:
        # TODO: logging in the future
        message += "<li>" + sentence + "</li>"

    message += "</ol></div>"

    # sends response back to the extension
    return json.dumps(message)


if __name__ == "__main__":
    app.run()
