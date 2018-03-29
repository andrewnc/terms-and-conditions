import json
import re
import requests
import sys

import unidecode
from bs4 import BeautifulSoup
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer

from preprocessing import prepare_for_regex

if sys.version_info >= (3, 0):
    from urllib.parse import unquote
else:
    from urlparse import unquote

# Globals
LANGUAGE = 'english'
SENTENCES_COUNT = 10

TERMS_PAGE_RE = re.compile(r"(terms *(((and|&)? *conditions)|((of)? ?(service|use))))", re.IGNORECASE)
HOST_RE = re.compile('(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*')
TERMS_LINK_RE = re.compile(r"(T|t)erms")
CLAUSE_RE = re.compile("(will)|(agree)|(must)|(responsib)|(waive)|(lawsuit)|(modify)|(intellec)", re.IGNORECASE)

# file structure for display, will update
HTML_OPEN = "<div id='mainPopup'>"
YOU_AGREE_HEADER = "<div id='youAgree' class='header'>What You Agree</div>"
THEY_AGREE_HEADER = "<div id='theyAgree' class='header'>What They Agree</div>"
OTHER_HEADER = "<div id='other' class='header'>Other Clauses</div>"


def summarize(html_body, url):
    html_soup = BeautifulSoup(html_body, "html.parser")
    body_txt = html_soup.text
    url = url.strip()

    is_terms_page = re.match(TERMS_PAGE_RE, body_txt)
    return summarize_terms_text(body_txt)


def find_terms_text(html_soup, url):
    host_url = re.search(HOST_RE, url).group(1)

    terms_text = ""
    for link in html_soup.find_all("a", text=TERMS_LINK_RE):
        if "http" in link['href']:
            soup = BeautifulSoup(requests.get(link['href']).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text
        else:
            soup = BeautifulSoup(requests.get("http://" + host_url + link['href']).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text

    if terms_text == "":
        print("googling", host_url)
        links = []
        google_results = BeautifulSoup(
            requests.get("https://www.google.com/search?q={}{}".format(host_url, "%20terms%20and%20conditions")).text,
            'html.parser')
        for link in google_results.find_all("div", {"class": "g"})[:1]:
            links.append(unquote(link.find("a").attrs['href'][7:].split("&")[0]))

        for link in links:
            soup = BeautifulSoup(requests.get(link).text, 'html.parser')
            soup = decomp(soup)
            terms_text += soup.text

    return terms_text


def summarize_terms_text(txt):
    text_data = unidecode.unidecode(txt)
    clean_list, pure_list = prepare_for_regex(text_data)

    data_to_summarize = []
    for clean, pure in zip(clean_list, pure_list):
        if re.findall(CLAUSE_RE, clean):
            data_to_summarize.append(pure)

    text_data = " ".join(data_to_summarize)
    parser = PlaintextParser(text_data, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = KLSummarizer(stemmer)

    summary = summarizer(parser.document, SENTENCES_COUNT)

    if len(summary) == 0:
        summary = ["No Terms found, if this is wrong, contact us at andrew@leaf.legal"]

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

    return json.dumps(message)


def decomp(soup):
    try:
        soup.footer.decompose()
    except:
        soup = soup
    try:
        soup.head.decompose()
    except:
        soup = soup
    try:
        for script in soup(["script", "style"]):
            script.decompose()  # rip it out
    except:
        soup = soup
    return soup
