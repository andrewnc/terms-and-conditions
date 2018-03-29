import json

from flask import Flask, request, render_template
from flask_cors import CORS

from summarizer import summarize

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def serve_homepage():
    return render_template("Legal Leaf.htm")


@app.route('/webapi/summarize', methods=['POST', 'GET', 'OPTIONS'])
def index():
    body_text = "".join(list(request.form.keys()) + list(request.form.values()))
    url = (request.headers.get("target_url")).strip()

    text = summarize(body_text, url)
    return json.dumps(text)


if __name__ == "__main__":
    app.run()
