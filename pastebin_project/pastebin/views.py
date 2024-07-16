from django.shortcuts import render, HttpResponse
from django.db import connections
from hashlib import md5
from sys import getsizeof
import html
import math
import re
import uuid
import base64


# Create your views here.

def escape_html_chars(text):
    return html.escape(text)


def sql_get_request(query, *args):
    cursor = connections['default'].cursor()
    cursor.execute(query, args)
    return cursor.fetchall()


def sql_post_request(query, *args):
    cursor = connections['default'].cursor()
    cursor.execute(query, args)


def size_converting(size_in_bytes):
    if size_in_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def url_generation():
    rv = base64.b64encode(uuid.uuid4().bytes).decode('utf-8')
    x = re.sub(r'[\=\+\/]', lambda m: {'+': '-', '/': '_', '=': ''}[m.group(0)], rv)
    return md5(x.encode()).hexdigest()  # mb I don't need this hash thing


def main_page(request):
    if request.method == 'POST':
        url = url_generation()
        text = request.POST['text'].encode('ascii', 'ignore').decode('ascii')
        languages = ['C', 'C#', 'C++', 'Go', 'Javascript', 'Css', 'Rust', 'Kotlin', 'Git', 'Python']
        if request.POST['lang'] in languages:
            sql_post_request("INSERT INTO pastes (url, data, lang) VALUES(%s, %s, %s);",
                             url, text, request.POST['lang'])
        else:
            sql_post_request("INSERT INTO pastes (url, data, lang) VALUES(%s, %s, 'none');", url, text)
        return HttpResponse(f'<script>document.location="{request.get_raw_uri() + url}";</script>')
    template_name = '../templates/pastebin/new_paste.html'
    return render(request, template_name)


def view_page(request):
    template_name = '../templates/pastebin/view_paste.html'
    if request.method == 'POST':
        url = request.POST['url']
        if not len(sql_get_request("SELECT lang FROM pastes WHERE url=%s", url)):
            return render(request, template_name, {'msg': 'This page/paste is not found..'})
        return HttpResponse(f'<script>document.location="/{url}";</script>')
    return render(request, template_name)


def paste_page(request, name):
    text = sql_get_request("SELECT data FROM pastes WHERE url=%s;", name)
    if len(text) == 0:
        return HttpResponse("Text box is empty. Something was wrong with your paste..")  # create html file with the same text but with background gif and other website style
    lang = sql_get_request("SELECT lang FROM pastes WHERE url=%s;", name)[0][0]
    text = escape_html_chars(text[0][0])
    text_size = size_converting(getsizeof(text))
    template_name = '../templates/pastebin/existing_paste.html'
    return render(request, template_name, {'url': name, 'size': text_size, 'lang': lang, 'paste': text })
