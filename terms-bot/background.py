import json
from flask import Flask,flash,get_flashed_messages, render_template, redirect, url_for, request
from flask_cors import CORS

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer

from sumy.summarizers.kl import KLSummarizer

# file structure for display, will update
HTML_OPEN = """
<!doctype html>
<head>
	<style type="text/css">
		#mainPopup {
			padding: 10px;
			height: 200px;
			width: 400px;
			font-family: Helvetica, Ubuntu, Arial, sans-serif;
		}
		h1 {
			font-size: 2em;
		}
	</style>
</head>
<div id="mainPopup">
	<h1>Welcome to legal summary bot</h1>"""


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/background.py', methods=['POST', 'GET', 'OPTIONS'])
def index():
	# globals
	LANGUAGE = 'english'
	SENTENCES_COUNT = 10

	# extract data from the extension
	re = request.form
	text_data = " ".join(list(re.keys()))

	# create parsers and summarize
	parser = PlaintextParser(text_data, Tokenizer(LANGUAGE))
	stemmer = Stemmer(LANGUAGE)
	summarizer = KLSummarizer(stemmer)

	# get summary
	summary = summarizer(parser.document, SENTENCES_COUNT)

	# return the summary sentences
	sentences = [str(x) for x in summary]
	message = HTML_OPEN + "\n<ol>"

	for sentence in sentences:
		# here we can do logging in the future
		print(sentence)
		message += "<li>" + sentence + "</li>"

	message += "</ol>\n</div>"

	with open("summary.html", 'w') as f:
		f.write(message)

	# sends response back to the extension
	return json.dumps(message)

if __name__ == "__main__":
	app.run()