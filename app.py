# coding: utf-8

from flask import Flask
from flask import render_template
from flask import jsonify

#from cocaine.services import Service

import pytz
import lxml
import lxml.html

from datetime import datetime
import urllib

app = Flask(__name__)

def fetchFromURL(url):
    #получаем страничку
    content = urllib.urlopen(url).read().decode('utf-8')

    return lxml.etree.HTML(content)

def getRooms(tree):
    titles = tree.xpath('//ul[@class="b-menu__layout"]//span[@class="b-link__inner"]/text()')
    rooms = tree.xpath('//div[@class="program"]//table[@class="hall-schedule"]')
    return zip(titles, rooms)

def getSchedule(room):
    for tr in room.xpath('.//tr'):
        tm = tr.xpath('string(.//td[1])')
        talk = unicode(tr.xpath('string(.//td[3]/div[@class="hall-schedule__talk-name"])'))
        yield datetime.strptime(tm, '%H:%M').time(), talk

@app.route('/')
def hello():
    tree = fetchFromURL('http://tech.yandex.ru/events/yac/2013/')
    rooms = getRooms(tree)

    def get_utc(t):
        tz = pytz.timezone('Europe/Moscow')
        return datetime.now(tz).replace(hour=t.hour, minute=t.minute).astimezone(pytz.utc)

    now = datetime.now(pytz.utc)

    res = [
        (title,
        [ (t, s) for t,s in getSchedule(r) if get_utc(t) > now])
        for title,r in rooms ]

    for _,d in res:
        for t, s in d:
            print t, get_utc(t)
        break

    return render_template('hello.html', data=res)


if __name__ == "__main__":
    app.run(debug=True)

