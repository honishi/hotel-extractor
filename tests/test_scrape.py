# -*- coding: utf-8 -*-

# import os

import pytest
import scrape


URL_IKKYU_ROUTE_INN_SAPPORO = "http://www.ikyu.com/biz/00080380/"
URL_IKKYU_THE_BEE_AKASAKA = "http://www.ikyu.com/biz/00080118/"
URL_IKKYU_NEW_OTANI =  "http://www.ikyu.com/biz/00080521/"
URL_IKKYU_APA_HOTEL_OSAKA_HIGO = "http://www.ikyu.com/biz/00080691/"
URL_IKKYU_REYZENIT_KINOSAKI = "http://www.ikyu.com/biz/00080672/"
URL_IKKYU_TOKYO_DAIICHI_OKINAWA = "http://www.ikyu.com/biz/00080828/"

URL_JALAN_ROUTE_INN_NAGOYA_SAKAE = "http://www.jalan.net/yad388438/"
URL_JALAN_MATSUKAZE = "http://www.jalan.net/yad327371/"
URL_JALAN_ORENOIE = "http://www.jalan.net/yad303074/"


# ikkyu tests
def test_ikkyu_search():
    info = scrape.search_ikkyu_hotels(u"ルートイン札幌")
    assert(info[0] == 3)
    assert(info[1] == u"ホテルルートイン札幌駅前北口")
    assert(info[2] == URL_IKKYU_ROUTE_INN_SAPPORO)

    info = scrape.search_ikkyu_hotels(u"ルートイン札幌北口")
    assert(info[0] == 1)
    assert(info[1] == u"ホテルルートイン札幌駅前北口")
    assert(info[2] == URL_IKKYU_ROUTE_INN_SAPPORO)

    info = scrape.search_ikkyu_hotels(u"あかさたな")
    assert(info[0] == 0)
    assert(info[1] is None)
    assert(info[2] is None)


def test_ikkyu_name():
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[0] == u"ホテルルートイン札幌駅前北口")


def test_ikkyu_address_tel():
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[1] == u"北海道北区北7条西4丁目2-2")
    assert(info[2] == u"011-727-2111")


def test_ikkyu_checkin():
    # 14:00
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_NEW_OTANI)
    assert(info[3] == u"14:00")

    # 15:00
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[3] == u"15:00")


def test_ikkyu_checkout():
    # 11:00
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_NEW_OTANI)
    assert(info[4] == u"11:00")

    # 10:00
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[4] == u"10:00")


def test_ikkyu_park():
    # 駐車場あり
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[5] == scrape.SERVICE_AVAILABLE)

    # 駐車場なし
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_THE_BEE_AKASAKA)
    assert(info[5] == scrape.SERVICE_UNAVAILABLE)


def test_ikkyu_room_service():
    # ルームサービスあり
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_NEW_OTANI)
    assert(info[6] == scrape.SERVICE_AVAILABLE)

    # ルームサービスあり
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[6] == scrape.SERVICE_UNAVAILABLE)


def test_ikkyu_esthetic():
    # エステ施設あり
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_APA_HOTEL_OSAKA_HIGO)
    assert(info[7] == scrape.SERVICE_AVAILABLE)

    # エステ施設なし
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[7] == scrape.SERVICE_UNAVAILABLE)


def test_ikkyu_fitness():
    # フィットネス施設あり
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_TOKYO_DAIICHI_OKINAWA)
    assert(info[8] == scrape.SERVICE_AVAILABLE)

    # フィットネス施設なし
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[8] == scrape.SERVICE_UNAVAILABLE)


def test_ikkyu_pet():
    # ペット受入可
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_REYZENIT_KINOSAKI)
    assert(info[9] == scrape.SERVICE_AVAILABLE)

    # ペット受け入れ不可
    info = scrape.scrape_ikkyu_hotel_details(URL_IKKYU_ROUTE_INN_SAPPORO)
    assert(info[9] == scrape.SERVICE_UNAVAILABLE)


# jalan tests
def test_jalan_search():
    info = scrape.search_jalan_hotels(u"ルートイン札幌")
    assert(info[0] == 4)
    assert(info[1] == u"ホテルルートイン札幌駅前北口")
    assert(info[2] == u"http://www.jalan.net/yad326777/")


def test_jalan_name():
    info = scrape.scrape_jalan_hotel_details(URL_JALAN_ROUTE_INN_NAGOYA_SAKAE)
    assert(info[0] == u"ホテルルートイン名古屋栄")


def test_jalan_internet():
    # インターネットあり
    info = scrape.scrape_jalan_hotel_details(URL_JALAN_ROUTE_INN_NAGOYA_SAKAE)
    assert(info[1] == scrape.SERVICE_AVAILABLE)

    info = scrape.scrape_jalan_hotel_details(URL_JALAN_MATSUKAZE)
    assert(info[1] == scrape.SERVICE_AVAILABLE)

    # インターネットなし
    info = scrape.scrape_jalan_hotel_details(URL_JALAN_ORENOIE)
    assert(info[1] == scrape.SERVICE_UNAVAILABLE)
