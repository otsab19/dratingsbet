#!/usr/bin/python3
import pudb
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
from yattag import indent
from lxml import etree

# define some constants
HEADER_FOOTBALL = ['Date','Away','Home','Odds to Win','ML Prediction','Score Proj','Total Goals']
PATH = ''

class DratingsBet():

    def __init__(self):
        self.links = []
        self.leagues = []
    def scrape_links(self):
        res = requests.get('https://www.dratings.com/')
        html_sel = html.fromstring(res.content)
        self.links = html_sel.xpath('//table[2]//tr/td/center/a/@href')
        self.leagues = html_sel.xpath('//table[2]//tr/td/center/a/text()')
        print(self.links)

    def start_requests(self):
        for links,league in zip(self.links,self.leagues):
            res = requests.get(links)
            html_sel = html.fromstring(res.content)
            # check tables for prediction table
            table = html_sel.xpath('//table')
            tab_tmp = list(table)
            for i, tab in enumerate(table):
                headers = html_sel.xpath('//table['+str(i+1)+']//tr//th/text()')
                if headers != HEADER_FOOTBALL:
                    tab_tmp.remove(tab)
            table = tab_tmp
            for index in range(len(table)):
                # particular tr
                data = html_sel.xpath('//table['+str(index+1)+']//tr[position()>1]')
                td = []
                for i in range(len(data)//3):
                    t = []
                    t = data[i*3:i*3+3:1]
                    td.append(t)
                for node in td:
                    li = {}
                    for i, nod in enumerate(node):
                        val_string = etree.tostring(nod)
                        val_ele = html.fromstring(val_string)
                        value = val_ele.xpath('//tr/td//text()')
                        print(value)
                        try:
                            li['sport'] = "Soccer"
                            li['League'] = league 
                            if i == 0:
                                li['Date'] = value[0]
                                li['Hometeam'] = value[2]
                                li['Awayteam'] = value[1]
                                li['Pred1'] = value[4]
                                #li['HomeTeamML'] = value[5]
                                li['Predtotalpointshome'] = value[6]
                                li['Predtotalpoints'] = value[7]
                            elif i==1:
                                li['Pred2'] = value[1]
                                #li['AwayTeamML'] = value[2]
                                li['Predtotalpointsaway'] = value[3]
                            else:
                                li['PredX'] = value[1]
                                #li['DawML'] = value[2]
                        except:
                            pass
                try:   
                    self.parse(li) 
                except:
                    pass
            # for node in data:
            #    # convert to string
            #    val_string = etree.tostring(node)
            #    # to element
            #    val_ele = html.fromstring(val_string)
            #    # extract list of text from td
            #    value = val_ele.xpath('//tr/td//text()')
            #    print(value)

    def parse(self, li):
        pudb.set_trace()
        root = Element('Matches')
        Match = SubElement(root, 'Match')
        Source = SubElement(Match, 'Source')
        Source.text = "Dratings"
        Sport = SubElement(Match, 'Sport')
        # Date = SubElement(Match, 'Date')
        Sport.text = li['sport']
        for elem in li:
            xml_attr = SubElement(Match, elem)
            xml_attr.text = li[elem]
        filename = li['Hometeam']+'-'+li['Awayteam']
        try:
            PATH = os.path.join(os.getcwd(), li['sport'])
            os.makedirs(PATH)
        except OSError as exc: 
            if exc.errno == errno.EEXIST and os.path.isdir(PATH):
                pass
            else:
                raise
        try:
            PATH = os.path.join(os.getcwd(), li['sport'],li['league'])
            os.makedirs(PATH)
        except OSError as exc: 
            if exc.errno == errno.EEXIST and os.path.isdir(PATH):
                pass
            else:
                raise
        # convert to lxml element to string    
        root_string = tostring(root)
        with open(os.path.join(PATH, filename), 'w', encoding="utf-8") as fl:
            print(filename)
            fl.write(indent(root_string.decode('utf-8')))


if __name__ == "__main__":
    ratings = DratingsBet()
    ratings.scrape_links()
    ratings.start_requests()
