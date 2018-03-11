import json
import re
import time

import requests
from bs4 import BeautifulSoup

from flask import Flask, request, render_template
from flask_cors import CORS
from preprocessing import prepare_for_regex
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer
# from sumy.summarizers.lex_rank import LexRankSummarizer as KLSummarizer

import unidecode
from urllib.parse import unquote

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
def decomp(soup):
    try:
        soup.footer.decompose()
    except:
        soup = soup
    try:
        soup.head.decompose()
    except:
        soup = soup
    return soup

@app.route('/background.py', methods=['POST', 'GET', 'OPTIONS'])
def index():
    # globals
    LANGUAGE = 'english'
    SENTENCES_COUNT = 10
    clause = re.compile("(reserves the right)|(loss)|(will)|(agree)|(must)|(responsib)|(waive)|(lawsuit)|(modify)|(intellec)")
    host_reg = re.compile('(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*')

    # extract data from the extension
    req = request.form
    url = " ".join(list(req.keys()) + list(req.values()))
    # logging can be done here

    url = url.strip()
    host_url = re.search(host_reg, url)['host']


    # I have moved scraping to the server side, it might be slower, but in the long run it will be much better imo, cause we can query cached values
    # get the home page and search for terms
    current_page_text = BeautifulSoup(requests.get(url).text, 'html.parser')
    # home_page_text = BeautifulSoup(requests.get("http://"+host_url).text, 'html.parser')
    links = []
    google_results = BeautifulSoup(requests.get("https://www.google.com/search?q={}{}".format(host_url, "%20terms%20and%20conditions")).text, 'html.parser')
    for link in google_results.find_all("div", {"class":"g"})[:1]:
        links.append(unquote(link.find("a").attrs['href'][7:].split("&")[0]))

    # print(links)
    # print(current_page_text, home_page_text)

    # print(current_page_text)
    # print(current_page_text.find_all("a", text=re.compile(r"(T|t)erms")))
    # check the current page for links if possible
    terms_text = ""
    for link in current_page_text.find_all("a", text=re.compile(r"(T|t)erms")):
        if "http" in link['href']:
            soup = BeautifulSoup(requests.get(link['href']).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text
        else:
            
            soup = BeautifulSoup(requests.get("http://"+host_url+link['href']).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text

    # # if we couldnt' find the terms there, check the home page
    # if terms_text == "":
    #     for link in home_page_text.find_all("a", text=re.compile(r"(T|t)erms")):
    #         if "http" in link['href']:
    #             terms_text += BeautifulSoup(requests.get(link['href']).text, 'html.parser').text
    #         else:
    #             terms_text += BeautifulSoup(requests.get("http://"+host_url+link['href']).text, 'html.parser').text
    if terms_text == "":
        for link in links:
            soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text
    
    text_data = unidecode.unidecode(terms_text)
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

    if len(summary) == 0:
        summary = ["No Terms"]

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
