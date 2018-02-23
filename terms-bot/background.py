import json
from flask import Flask,flash,get_flashed_messages, render_template, redirect, url_for, request
from flask_cors import CORS

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

from sumy.summarizers.kl import KLSummarizer

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/background.py', methods=['POST', 'GET', 'OPTIONS'])
def index():
	# globals
	LANGUAGE = 'english'
	SENTENCES_COUNT = 10

	# extract data from the extension
	re = request.form
	text_data = list(re.keys())[0]

	# create parsers and summarize
	parser = PlaintextParser(text_data, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = KLSummarizer(stemmer)

	# show summary
	summary = summarizer(parser.document, SENTENCES_COUNT)
	for sentence in summary:
		print(sentence, end="\n\n")

	# return the summary sentences
	return json.dumps([" ".join(x.words) for x in summary])

if __name__ == "__main__":
	app.run()