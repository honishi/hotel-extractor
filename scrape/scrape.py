# coding: UTF-8

import re
import urllib2

import requests
from pyquery import PyQuery as pq


SERVICE_AVAILABLE = u"YES"
SERVICE_UNAVAILABLE = u"NO"
SERVICE_UNKNOWN = u"UNKNOWN"

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36")

# ikkyu
URL_IKKYU_HOTEL_QUERY = "http://www.ikyu.com/ap/srch/UspW11103.aspx?kwd="

SELECTOR_IKKYU_HIT_COUNT         = "#ctl00_contentMain_KeywordAccommodationListUserControl1_DivKeyWord"
SELECTOR_IKKYU_HOTEL_NAME        = "#ctl00_contentMain_KeywordAccommodationListUserControl1_ctl01_TriesteLabelAccommodationNm"
SELECTOR_IKKYU_HOTEL_LINK        = "#ctl00_contentMain_KeywordAccommodationListUserControl1_ctl01_TriesteHyperLinkAccommodationNm"

SELECTOR_IKKYU_HOTEL_NAME_DETAIL = "#ctl00_contentMain_AccommodationInfoPartAccommodationNmUserControl1_AcmNm"
SELECTOR_IKKYU_ADDRESS_PREF      = "#ctl00_contentMain_AccommodationInfoPartAddressAndTelUserControl1_LblPref"
SELECTOR_IKKYU_ADDRESS_ADDRESS   = "#ctl00_contentMain_AccommodationInfoPartAddressAndTelUserControl1_LblAddress"
SELECTOR_IKKYU_TEL               = "#ctl00_contentMain_AccommodationInfoPartAddressAndTelUserControl1_LblTel"
SELECTOR_IKKYU_CHECKIN           = "#ctl00_contentMain_AccommodationInfoPartTableUserControl1_LblChkinTime"
SELECTOR_IKKYU_CHECKOUT          = "#ctl00_contentMain_AccommodationInfoPartTableUserControl1_LblChkoutTime"
SELECTOR_IKKYU_PARK              = "#ctl00_contentMain_AccommodationInfoPartTableUserControl1_LblCarCount"
SELECTOR_IKKYU_ROOM_SERVICE      = "#ctl00_contentMain_AccommodationInfoPartTableUserControl1_LblRoomSvc"
SELECTOR_IKKYU_ESTHE             = "#ctl00_contentMain_AccommodationInfoPartIconsUserControl1_ImgEsthetique"
SELECTOR_IKKYU_FITNESS           = "#ctl00_contentMain_AccommodationInfoPartIconsUserControl1_ImgFitness"
SELECTOR_IKKYU_PET               = "#ctl00_contentMain_AccommodationInfoPartIconsUserControl1_ImgPetTolerance"

# jalan
URL_JALAN_HOTEL_SEARCH = "http://www.jalan.net/uw/uwp2011/uww2011init.do?keyword="
URL_JALAN_HOTEL_DETAIL = "http://www.jalan.net/yad"

SELECTOR_JALAN_HIT_COUNT         = ".s18_f60b"
SELECTOR_JALAN_HOTEL_NAME        = ".s16_33b"
SELECTOR_JALAN_HOTEL_LINK        = SELECTOR_JALAN_HOTEL_NAME

SELECTOR_JALAN_HOTEL_NAME_DETAIL = "#yado_header_hotel_name"
SELECTOR_JALAN_INTERNET          = ".td01"


# ikkyu scraper
def search_ikkyu_hotels(hotel_name):
    list_url = URL_IKKYU_HOTEL_QUERY + hotel_name
    request = requests.get(list_url, headers={"User-Agent": USER_AGENT})
    if request.status_code != 200:
        raise Exception()

    content = request.content
    query = pq(content)

    hit_count = 0
    name = None
    url = None

    hit_count_text = query(SELECTOR_IKKYU_HIT_COUNT).text()
    matched = re.match(ur".*（\s*(\d+)\s*件）", hit_count_text, re.UNICODE)
    if matched:
        hit_count = int(matched.group(1))

    if 0 < hit_count:
        name = query(SELECTOR_IKKYU_HOTEL_NAME).text()
        url = query(SELECTOR_IKKYU_HOTEL_LINK).attr['href']

    return hit_count, name, url, list_url


def scrape_ikkyu_hotel_details(url):
    request = requests.get(url, headers={"User-Agent": USER_AGENT})
    if request.status_code != 200:
        raise Exception()

    content = request.content
    # text = request.text

    query = pq(content)

    name = query_name(query)
    address = query_address(query)
    tel = query_tel(query)
    checkin = query_checkin(query)
    checkout = query_checkout(query)
    park = query_park(query)
    room_service = query_room_service(query)
    esthetic = query_esthetic(query)
    fitness = query_fitness(query)
    pet = query_pet(query)

    info = name, address, tel, checkin, checkout, park, room_service, esthetic, fitness, pet

    return info


def query_name(query):
    name = query(SELECTOR_IKKYU_HOTEL_NAME_DETAIL).text()
    return name


def query_address(query):
    address = (query(SELECTOR_IKKYU_ADDRESS_PREF).text() + query(SELECTOR_IKKYU_ADDRESS_ADDRESS).text())
    return address


def query_tel(query):
    text = query(SELECTOR_IKKYU_TEL).text()
    tel = text

    matched = re.match(ur"TEL (.+)", text)
    if matched:
        tel = matched.group(1)

    return tel


def query_checkin(query):
    text = query(SELECTOR_IKKYU_CHECKIN).text()

    # expected format: "14:00～29:00"
    checkin = re.match(r"(\d+:\d+).*", text).group(1)

    return checkin


def query_checkout(query):
    text = query(SELECTOR_IKKYU_CHECKOUT).text()
    return text


def query_park(query):
    park = SERVICE_UNKNOWN
    text = query(SELECTOR_IKKYU_PARK).text()

    if re.search(ur".*\d{1,3}台.*", text) is not None:
        park = SERVICE_AVAILABLE
    else:
        park = SERVICE_UNAVAILABLE

    return park


def query_room_service(query):
    room_service = SERVICE_UNKNOWN
    text = query(SELECTOR_IKKYU_ROOM_SERVICE).text()

    if re.search(ur"ご利用いただけます", text):
        room_service = SERVICE_AVAILABLE
    elif re.search(ur"ご利用いただけません", text):
        room_service = SERVICE_UNAVAILABLE

    return room_service


def query_esthetic(query):
    esthe = SERVICE_UNKNOWN
    alt = query(SELECTOR_IKKYU_ESTHE).attr['alt']

    if alt == u"エステ施設あり":
        esthe = SERVICE_AVAILABLE
    elif alt == u"エステ施設なし":
        esthe = SERVICE_UNAVAILABLE

    return esthe


def query_fitness(query):
    fitness = SERVICE_UNKNOWN
    alt = query(SELECTOR_IKKYU_FITNESS).attr['alt']

    if alt == u"フィットネス施設あり":
        fitness = SERVICE_AVAILABLE
    elif alt == u"フィットネス施設なし":
        fitness = SERVICE_UNAVAILABLE

    return fitness


def query_pet(query):
    pet = SERVICE_UNKNOWN
    alt = query(SELECTOR_IKKYU_PET).attr['alt']

    if alt == u"ペット受入可":
        pet = SERVICE_AVAILABLE
    elif alt == u"ペット受入不可":
        pet = SERVICE_UNAVAILABLE

    return pet


# jalan scraper
def search_jalan_hotels(hotel_name):
    list_url = URL_JALAN_HOTEL_SEARCH + urllib2.quote(hotel_name.encode('shift-jis'))
    request = requests.get(list_url, headers={"User-Agent": USER_AGENT})
    if request.status_code != 200:
        raise Exception()

    request.encoding = 'shift_jis'
    text = request.text
    query = pq(text)

    hit_count = 0
    name = None
    url = None

    hit_count_text = query(SELECTOR_JALAN_HIT_COUNT).text()
    if hit_count_text != '':
        hit_count = int(hit_count_text)

    if 0 < hit_count:
        name = query(SELECTOR_JALAN_HOTEL_NAME).eq(0).text()

        href = query(SELECTOR_JALAN_HOTEL_LINK).eq(0).find('a').attr['href']
        matched = re.match(r".*\('(\d+)'\)", href)
        if matched:
            url = URL_JALAN_HOTEL_DETAIL + matched.group(1) + '/'

    return hit_count, name, url, list_url


def scrape_jalan_hotel_details(url):
    request = requests.get(url, headers={"User-Agent": USER_AGENT})
    if request.status_code != 200:
        raise Exception()

    request.encoding = 'shift_jis'
    text = request.text
    query = pq(text)

    name = query_jalan_name(query)
    internet = query_internet(query)

    info = name, internet

    return info


def query_jalan_name(query):
    name = query(SELECTOR_JALAN_HOTEL_NAME_DETAIL).find('a').text()
    return name


def query_internet(query):
    internet = SERVICE_UNAVAILABLE

    rows = query(SELECTOR_JALAN_INTERNET)

    for row in rows.items():
        if row.text() == u"インターネット関連":
            for sibling in row.siblings():
                description = sibling.text
                searched = re.search(ur"全室対応", description)
                if searched:
                    internet = SERVICE_AVAILABLE
                    break

    return internet
