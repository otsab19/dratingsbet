#!/usr/bin/python
import os
import re
import sys
parent_dir = os.path.abspath(os.path.dirname('dratings.py'))
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from lxml import html
import multiprocessing
import json
import csv
import xml
import datetime
import requests
from bs4 import BeautifulSoup
from dateutil.rrule import rrule, DAILY
import errno
#from yattag import indent
from lxml import etree
class DratingsBet():

    def __init__(self):
        self.links = []

    def scrape_links(self):
        res = requests.get('https://www.dratings.com/')
        html_sel = html.fromstring(res.content)
        self.links = html_sel.xpath('//table[2]//tr/td/center/a/@href')
        print(self.links)

    def start_requests(self):
        for links in self.links:
            res = requests.get(links)
            html_sel = html.fromstring(res.content)
            # particular tr
            data = html_sel.xpath('//table[1]//tr[positon()>1]')
            td=[]
            for i in range(len(data)//3):
                t = []
                t = data[i*3:i*3+3:1]
                td.append(t)
            for node in data:
                # convert to string
                val_string = etree.tostring(node)
                # to element
                val_ele = html.fromstring(val_string)
                # extract list of text from td
                value = val_ele.xpath('//tr/td//text()')
                print(value)

    # def parse():


if __name__ == "__main__":
    ratings = DratingsBet()
    ratings.scrape_links()
    ratings.start_requests()
