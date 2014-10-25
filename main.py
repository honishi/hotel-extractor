# coding: UTF-8

from flask import Flask
from flask import request
from flask import render_template

import scrape


app = Flask(__name__)
app.debug = True


@app.route('/')
def top():
    return render_template('info.html',
                           ikkyu_search_result=None,
                           ikkyu_info=None,
                           jalan_search_result=None,
                           jalan_info=None)


@app.route('/query', methods=['POST'])
def query():
    hotel_name = request.form['hotel_name']

    ikkyu_search_result, ikkyu_info = query_ikkyu(hotel_name)
    jalan_search_result, jalan_info = query_jalan(hotel_name)

    return render_template('info.html',
                           ikkyu_search_result=ikkyu_search_result,
                           ikkyu_info=ikkyu_info,
                           jalan_search_result=jalan_search_result,
                           jalan_info=jalan_info)


def query_ikkyu(hotel_name):
    search_result = scrape.search_ikkyu_hotels(hotel_name)

    info = None
    if 0 < search_result[0]:
        info = scrape.scrape_ikkyu_hotel_details(search_result[2])

    return search_result, info


def query_jalan(hotel_name):
    search_result = scrape.search_jalan_hotels(hotel_name)

    info = None
    if 0 < search_result[0]:
        info = scrape.scrape_jalan_hotel_details(search_result[2])

    return search_result, info
