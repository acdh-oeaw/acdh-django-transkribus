import json
import requests
import lxml.etree as ET

from django.conf import settings

base_url = "https://transkribus.eu/TrpServer/rest"
nsmap = {
    "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
}

try:
    user = settings.TRANSKRIBUS['user']
except KeyError:
    print("no TRANSKRIBUS user set in the project's settings file")
    user = "user"

try:
    pw = settings.TRANSKRIBUS['pw']
except KeyError:
    print("no TRANSKRIBUS pw set in the project's settings file")
    pw = "pw"

try:
    col_id = settings.TRANSKRIBUS['col_id']
except KeyError:
    print("no TRANSKRIBUS col_id set in the project's settings file")
    col_id = None


try:
    base_url = settings.TRANSKRIBUS['base_url']
except KeyError:
    base_url = "https://transkribus.eu/TrpServer/rest"


def trp_login(user, pw, base_url=base_url):
    url = "{}/auth/login".format(base_url)
    payload = "user={}&pw={}".format(user, pw)
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    if response.ok:
        session_id = response.text.split('<sessionId>')[1].split('</sessionId>')[0]
        return session_id
    else:
        response.ok


def trp_ft_search(base_url=base_url, user=user, pw=pw, **kwargs):
    url = f"{base_url}/search/fulltext"
    if kwargs:
        querystring = kwargs
    else:
        return False
    querystring['type'] = "LinesLc"
    print(querystring)
    session_id = trp_login(user, pw, base_url=base_url)
    headers = {
        'cookie': "JSESSIONID={}".format(session_id),
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.ok:
        return response.json()
    else:
        return response.ok


def trp_get_fulldoc_md(doc_id, base_url=base_url, col_id=col_id, page_id="1", user=user, pw=pw):
    url = f"{base_url}/collections/{col_id}/{doc_id}/{page_id}"
    session_id = trp_login(user, pw, base_url=base_url)
    headers = {
        'cookie': "JSESSIONID={}".format(session_id),
    }
    response = requests.request("GET", url, headers=headers)
    if response.ok:
        doc_xml = ET.fromstring(response.text.encode('utf8'))
        result = {
            "doc_id": doc_id,
            "base_url": base_url,
            "col_id": col_id,
            "page_id": page_id,
            "session_id": session_id
        }
        result["doc_url"] = url
        result["doc_xml"] = doc_xml
        result["transcript_url"] = doc_xml.xpath('//tsList/transcripts[1]/url/text()')[0]
        result["thumb_url"] = doc_xml.xpath('./thumbUrl/text()')[0]
        result["img_url"] = doc_xml.xpath('./url/text()')[0]
        result["img_url"] = doc_xml.xpath('./url/text()')[0]
        return result
    else:
        return response.ok


def get_transcript(fulldoc_md):
    nsmap = nsmap = {
        "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
    }
    md = fulldoc_md
    url = md['transcript_url']
    headers = {
        'cookie': "JSESSIONID={}".format(md['session_id']),
    }
    response = requests.request("GET", url, headers=headers)
    if response.ok:
        page = ET.fromstring(response.text.encode('utf8'))
        md['page_xml'] = page
        md['transcript'] = page.xpath(
            './/page:TextLine//page:Unicode/text()', namespaces=nsmap
        )
        return md
    else:
        return response.ok


def list_documents(base_url=base_url, col_id=col_id, user=user, pw=pw):
    url = f"{base_url}/collections/{col_id}/list"
    session_id = trp_login(user, pw, base_url=base_url)
    headers = {
        'cookie': "JSESSIONID={}".format(session_id),
    }
    response = requests.request("GET", url, headers=headers)
    if response.ok:
        return response.json()
    else:
        return response.ok
