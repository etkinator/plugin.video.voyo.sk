# -*- coding: utf-8 -*-
import json
import os
import pickle
import re
import sqlite3
import sys
import urllib
from datetime import datetime
from urllib import parse

import inputstreamhelper
import requests
import routing
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
from bs4 import BeautifulSoup

_addon = xbmcaddon.Addon()
_profile = xbmcvfs.translatePath( _addon.getAddonInfo('profile'))
plugin = routing.Plugin()

_UserAgent_ = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'
_baseurl = 'https://voyo.markiza.sk/'


#------------------------------Menu--------------------------------------
@plugin.route('/list_home/<type>')
def list_home(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    listing = []
    #pokurl=build_url({'mode':'folder', 'foldername':'Folder One' })
    #print(pokurl)
    soup = get_page(_baseurl+'home')
    articles = soup.find_all('section', {'class': 'c-section'})
    print(articles)
    for article in articles:
        try:
            try:
                title = article.header.h2.a.contents[0].encode('utf-8').strip()
            except:
                title = article.header.h2.contents[0].encode('utf-8').strip()
            print(title)
            skup=article.div
            print(skup)
            list_item = xbmcgui.ListItem(label=title)
            list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
            list_item.setArt({'icon': 'DefaultMovies.png'})
            listing.append((plugin.url_for(get_listH, show_skup = skup, categorie = title), list_item, True))
        except:
            title=''

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_news/<type>')
def list_news(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    listing = []
    #pokurl=build_url({'mode':'folder', 'foldername':'Folder One' })
    #print(pokurl)
    soup = get_page(_baseurl+'novinky')
    articles = soup.find_all('section', {'class': 'c-section'})
    print(articles)
    for article in articles:
        try:
            try:
                title = article.header.h2.a.contents[0].encode('utf-8').strip()
            except:
                title = article.header.h2.contents[0].encode('utf-8').strip()
            print(title)
            skup=article.div
            print(skup)
            list_item = xbmcgui.ListItem(label=title)
            list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
            list_item.setArt({'icon': 'DefaultMovies.png'})
            listing.append((plugin.url_for(get_listH, show_skup = skup, categorie = title), list_item, True))
        except:
            title=''

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/list_movies/<type>')	
def list_movies(type):
    xbmcplugin.setContent(plugin.handle, 'films')
    soup = get_page(_baseurl+'filmy')
    listing = []
    articles = soup.find_all('a', {'class': 'dropdown-item'})
    for article in articles:
        title=article.contents[0].encode('utf-8').lstrip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        #info=get_infoM(article.h3.a['href'])
        #info.update({'mediatype': 'movie', 'title': title})
        #list_item.setInfo('video', info)
        list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
        list_item.setArt({'icon': 'DefaultMovies.png'})
        listing.append((plugin.url_for(get_list, show_url = article['href'], next_state = False), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_serials/<type>')
def list_serials(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    soup = get_page(_baseurl+'serialy/')
    listing = []
    articles = soup.find_all('a', {'class': 'dropdown-item'})
    for article in articles:
        title=article.contents[0].encode('utf-8').lstrip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
        list_item.setArt({'icon': 'DefaultMovies.png'})
        listing.append((plugin.url_for(get_list, show_url = article['href'], next_state = False), list_item, True))
    
    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_shows/<type>')
def list_shows(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    soup = get_page(_baseurl+'relacie')
    listing = []
    articles = soup.find_all('a', {'class': 'dropdown-item'})
    for article in articles:
        title=article.contents[0].encode('utf-8').lstrip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
        list_item.setArt({'icon': 'DefaultMovies.png'})
        listing.append((plugin.url_for(get_list, show_url = article['href'], next_state = False), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_kids/<type>')
def list_kids(type):
    xbmcplugin.setContent(plugin.handle, 'films')
    soup = get_page(_baseurl+'/deti')
    listing = []
    articles = soup.find_all('a', {'class': 'dropdown-item'})
    for article in articles:
        title=article.contents[0].encode('utf-8').lstrip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
        list_item.setArt({'icon': 'DefaultMovies.png'})
        listing.append((plugin.url_for(get_list, show_url = article['href'], next_state = False), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_sport/<type>')
def list_sport(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    soup = get_page(_baseurl+'sport')
    listing = []
    articles = soup.find_all('a', {'class': 'dropdown-item'})
    for article in articles:
        title=article.contents[0].encode('utf-8').lstrip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
        list_item.setArt({'icon': 'DefaultMovies.png'})
        listing.append((plugin.url_for(get_list, show_url = article['href'], next_state = False), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/list_search/<type>')
def list_search(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    listing = []
    searchin = xbmcgui.Dialog()
    search = searchin.input(_addon.getLocalizedString(30008)) #'Hledat'
    #url='https://voyo.markiza.sk/api/v1/search'
    #par={'query':search, 'filter':'show'}
    #soup = get_next_page(url=url, par=par)
    soup = get_page('https://voyo.markiza.sk/api/v2/search?query='+search+'&filter=show')
    print(soup)
    articles = soup.find_all('article', {'class': 'c-video-box'})
    print(articles)
    for article in articles:
        title = article.h3.a.contents[0].encode('utf-8').strip()
        print(title)
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
        if str(article.h3.a['href']).find('/filmy/')>0 :
            #print('filmy get')
            if str(article.h3.a['href']).find('/kolekcie/')>0 :
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listMKol, show_url = article.h3.a['href']), list_item, True))
            else:
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
        elif str(article.h3.a['href']).find('/relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                print('serial epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                print('serial kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                print('serial get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy-a-relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                print('serialy-a-relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                print('serialy-a-relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                print('serialy-a-relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        else:
            xbmcgui.Dialog().notification(_addon.getAddonInfo('name'),_addon.getLocalizedString(30100), xbmcgui.NOTIFICATION_ERROR, 5000) #'Nenájdené'

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)



@plugin.route('/list_HistView/<type>')
def list_HistView(type):
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    listing = []

    recs=SqlRun( mode='read_all', title=None, url=None, url_img=None, data=None)
    print(recs)

        #sqlite_create_table_query = '''CREATE TABLE if not exists Hist_View (
        #                            id INTEGER PRIMARY KEY,
        #                            title TEXT NOT NULL UNIQUE,
        #                            url TEXT NOT NULL,
        #                            url_img TEXT NOT NULL,
        #                            mediatype text,
        #                            plot text,
        #                            duration text,
        #                            year text,
        #                            dataum datetime);'''
        #data={'mediatype': medtyp, 'title': title, 'plot' : desc, 'year' : year, 'duration': tim}



    for rec in recs:
        print(rec)
        print("Id: ", rec[0])
        print("title: ", rec[1])
        print("url: ", rec[2])
        print("url_img: ", rec[3])
        print("mediatype: ", rec[4])
        print("plot: ", rec[5])
        print("duration: ", rec[6])
        print("year: ", rec[7])
        print("datum: ", rec[8])
        print("\n")
        url=rec[2]
        #datac=str_to_class(rec[4])
        #print(datac)
        title=rec[1]
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'poster': rec[3], 'icon': rec[3]})
        list_item.setInfo('video', {'mediatype': rec[4], 'title': title, 'plot' : rec[5], 'year' : int(rec[7]), 'duration': int(rec[6])})
        #list_item.setInfo('video', {'mediatype': 'video', 'title': title})

        if str(url).find('/filmy/')>0 :
            #print('filmy get')
            if str(url).find('/kolekcie/')>0 :
                listing.append((plugin.url_for(get_listMKol, show_url = url), list_item, True))
            else:
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, url), list_item, False))
        elif str(url).find('/relacie/')>0 :
            if str(url).find('/epizoda/')>0 :
                #print('relacie epizoda get')
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, url), list_item, False))
            elif str(url).find('/kolekcie/')>0 :
                #print('relacie kolekcie get')
                listing.append((plugin.url_for(get_listSKol, show_url = url), list_item, True))
            else:
                #print('relacie get')
                listing.append((plugin.url_for(get_listSez, show_url = url), list_item, True))
        elif str(url).find('/serialy/')>0 :
            if str(url).find('/epizoda/')>0 :
                #print('serial epizoda get')
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, url), list_item, False))
            elif str(url).find('/kolekcie/')>0 :
                #print('serial kolekcie get')
                listing.append((plugin.url_for(get_listSKol, show_url = url), list_item, True))
            else:
                #print('serial get')
                listing.append((plugin.url_for(get_listSez, show_url = url), list_item, True))
        elif str(url).find('/serialy-a-relacie/')>0 :
            if str(url).find('/epizoda/')>0 :
                #print('serialy-a-relacie epizoda get')
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, url), list_item, False))
            elif str(url).find('/kolekcie/')>0 :
                #print('serialy-a-relacie kolekcie get')
                listing.append((plugin.url_for(get_listSKol, show_url = url), list_item, True))
            else:
                #print('serialy-a-relacie get')
                listing.append((plugin.url_for(get_listSez, show_url = url), list_item, True))
        else:
            xbmcgui.Dialog().notification(_addon.getAddonInfo('name'),_addon.getLocalizedString(30100), xbmcgui.NOTIFICATION_ERROR, 5000) #'Nenájdené'



        #list_item.setProperty('IsPlayable', 'true')
        #listing.append((plugin.url_for(get_list, rec[2]), list_item, False))


    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

#------------------------------kategorie--------------------------------------


@plugin.route('/get_listH/')
def get_listH():
    xbmcplugin.setContent(plugin.handle, 'videos')
    listing = []
    sku=plugin.args['show_skup'][0]
    print(sku)
    skup = BeautifulSoup(plugin.args['show_skup'][0], 'html.parser')
    categorie= plugin.args['categorie'][0]
    #print(skup)
    articles= skup.find_all('article', {'class': 'c-video-box'})
    #print(articles)
    for article in articles:
        title = str(article.h3.a.contents[0].strip()) #.encode('utf-8')
        title = ''.join(title.split('\n'))
        #print(title)
        list_item = xbmcgui.ListItem(label=title)
        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
        if categorie == 'Dříve než v TV':   
            title = ''.join(title.split(' '))
            title = ' - '.join(title.split('-'))
        ind=str(article.h3.a['href']).find('filmy/')
        #print(ind)
        if str(article.h3.a['href']).find('/filmy/')>0 :
            #print('filmy get')
            if str(article.h3.a['href']).find('/kolekcie/')>0 :
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listMKol, show_url = article.h3.a['href']), list_item, True))
            else:
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
        elif str(article.h3.a['href']).find('/relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('serial epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('serial kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('serial get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy-a-relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('serialy-a-relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('serialy-a-relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('serialy-a-relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        else:
            xbmcgui.Dialog().notification(_addon.getAddonInfo('name'),_addon.getLocalizedString(30100), xbmcgui.NOTIFICATION_ERROR, 5000) #'Nenájdené'

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)




@plugin.route('/get_list/')
def get_list():
    xbmcplugin.setContent(plugin.handle, 'videos')
    url = plugin.args['show_url'][0]
    nextS = plugin.args['next_state'][0]
    listing = []
    if nextS:
        payload = get_bpar(url) #{'category': 'voyo-3', 'sort': 'title__asc', 'limit': '24', 'page': '2' }
        url_send= get_burl(url)
        soup = get_next_page(url=url_send, par=payload)
    else:
        soup = get_page(url)
    articles = soup.find_all('div', {'class': 'c-video-box'})
    for article in articles:
        title = article.h3.a.contents[0].encode('utf-8').strip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)

        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})

        if str(article.h3.a['href']).find('/filmy/')>0 :
            #print('filmy get')
            if str(article.h3.a['href']).find('/kolekcie/')>0 :
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listMKol, show_url = article.h3.a['href']), list_item, True))
            else:
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
        elif str(article.h3.a['href']).find('/relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('serial epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('serial kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('serial get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        elif str(article.h3.a['href']).find('/serialy-a-relacie/')>0 :
            if str(article.h3.a['href']).find('/epizoda/')>0 :
                #print('serialy-a-relacie epizoda get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                list_item.setProperty('IsPlayable', 'true')
                listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
            elif str(article.h3.a['href']).find('/kolekcie/')>0 :
                #print('serialy-a-relacie kolekcie get')
                list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
                listing.append((plugin.url_for(get_listSKol, show_url = article.h3.a['href']), list_item, True))
            else:
                #print('serialy-a-relacie get')
                list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
                listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))
        else:
            xbmcgui.Dialog().notification(_addon.getAddonInfo('name'),_addon.getLocalizedString(30100), xbmcgui.NOTIFICATION_ERROR, 5000) #'Nenájdené'
        #else:
        #    #print('serial get')
        #    list_item.setInfo('video', {'mediatype': 'tvshow', 'title': title})
        #    listing.append((plugin.url_for(get_listSC, category = True, show_url = article.h3.a['href'], showtitle = title), list_item, True))

    next = soup.find('div', {'class': 'load-more'})
    if next:
        list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30010))
        #listing.append((plugin.url_for(get_list, show_url = next.find('button')['data-href'], next_state = True), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)


#@plugin.route('/get_listMN/')
#def get_listMN():
#    xbmcplugin.setContent(plugin.handle, 'videos')
#    url = plugin.args['show_url'][0]
#    payload = get_bpar(url) #{'category': 'voyo-3', 'sort': 'title__asc', 'limit': '24', 'page': '2' }
#    url_send= get_burl(url)
#    soup = get_next_page(url=url_send, par=payload)
#    listing = []
#    articles = soup.find_all('div', {'class': 'c-video-box'})
#    for article in articles:
#        title = article.h3.a.contents[0].encode('utf-8')
#        list_item = xbmcgui.ListItem(label=title.strip())
#        print(title)
#        #info=get_infoM(article.h3.a['href'])
#        #info.update({'mediatype': 'movie', 'title': title})
#        #list_item.setInfo('video', info)
#        if str(article.h3.a['href']).find('/kolekcie/')>0 :
#            list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
#            list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
#            listing.append((plugin.url_for(get_listMKol, show_url = article.h3.a['href']), list_item, False))
#        else:
#            list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
#            list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
#            list_item.setProperty('IsPlayable', 'true')
#            listing.append((plugin.url_for(get_video2, article.h3.a['href']), list_item, False))
#    next = soup.find('div', {'class': 'load-more'})
#    if next:
#        list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30004))
#        listing.append((plugin.url_for(get_listMN, show_url = next.find('button')['data-href']), list_item, True))
#
#    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
#    xbmcplugin.endOfDirectory(plugin.handle)





#------------------------------filmy/pořad/serial--------------------------------------
#------------------------------filmy/kolekcie--------------------------------------
@plugin.route('/get_listMKol/')
def get_listMKol():
    xbmcplugin.setContent(plugin.handle, 'videos')
    url = plugin.args['show_url'][0]
    soup = get_page(url)
    print(soup)
    listing = []
    articles = soup.find_all('article', {'class': 'c-video-box'})
    print(articles)
    for article in articles:
        title = article.h3.a.contents[0].encode('utf-8').strip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        #info=get_infoM(article.h3.a['href'])
        #info.update({'mediatype': 'movie', 'title': title})
        #list_item.setInfo('video', info)
        list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
        list_item.setProperty('IsPlayable', 'true')
        listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

#------------------------------serial/sezona+kolekcie+epizoda--------------------------------------
@plugin.route('/get_listSez/')
def get_listSez():
    print('Sez')
    xbmcplugin.setContent(plugin.handle, 'tvshows')
    listing = []  
    url = plugin.args['show_url'][0]
    soup = get_page(url)
    articles = soup.find_all('a', {'href':'#seasons'})
    articlesimg = soup.find('img', {'class':'img-fluid lazyload'})
    img=articlesimg['data-src']
    print(img)
    for article in articles:
        titlep = article.contents[0]
        number=article.span.contents[0]
        title=titlep+', '+number+' dílů'
        list_item = xbmcgui.ListItem(label=title.strip())
        #list_item.setInfo('video', {'mediatype': 'episode', 'tvshowtitle': showtitle, 'title': title, 'duration': dur})
        list_item.setInfo('video', {'mediatype': 'episode', 'title': title})
        list_item.setArt({'poster': img, 'icon': img})
        url=_baseurl+article['data-replace-url']
        listing.append((plugin.url_for(get_listEp, show_url = url, next_state = False), list_item, True))
 
    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/get_listEp/')
def get_listEp():
    xbmcplugin.setContent(plugin.handle, 'episodes')
    listing = []  
    url = plugin.args['show_url'][0]
    nextS = plugin.args['next_state'][0]
    if nextS:
        payload = get_bpar(url) #{'category': 'voyo-3', 'sort': 'title__asc', 'limit': '24', 'page': '2' }
        url_send= get_burl(url)
        soup = get_next_page(url=url_send, par=payload)
    else:
        soup = get_page(url)
    articles = soup.find_all('article', 'c-video-box -media -alt')
    print(articles)
    count = 0
    for article in articles:
        title = article.h3.a.contents[0].strip()
        list_item = xbmcgui.ListItem(title)
        list_item.setInfo('video', {'mediatype': 'episode', 'title': title})
        #list_item.setArt({'': article.img['data-src']})
        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
        list_item.setProperty('IsPlayable', 'true')
        listing.append((plugin.url_for(get_video, article.h3.a['href']), list_item, False))
        count +=1
    next = soup.find('div', {'class': 'load-more'})
    if next:
        list_item = xbmcgui.ListItem(label=_addon.getLocalizedString(30010))
        listing.append((plugin.url_for(get_listEp, show_url = next.find('button')['data-href'], next_state = True), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)

@plugin.route('/get_listSKol/')
def get_listSKol():
    print('1')
    xbmcplugin.setContent(plugin.handle, 'videos')
    print
    url = plugin.args['show_url'][0]
    soup = get_page(url)
    print(soup)
    listing = []
    articles = soup.find_all('article', {'class': 'c-video-box'})
    print(articles)
    for article in articles:
        title = article.h3.a.contents[0].encode('utf-8').strip()
        list_item = xbmcgui.ListItem(label=title)
        print(title)
        #info=get_infoM(article.h3.a['href'])
        #info.update({'mediatype': 'movie', 'title': title})
        #list_item.setInfo('video', info)
        list_item.setInfo('video', {'mediatype': 'movie', 'title': title})
        list_item.setArt({'poster': article.img['data-src'], 'icon': article.img['data-src']})
        listing.append((plugin.url_for(get_listSez, show_url = article.h3.a['href']), list_item, True))

    xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
    xbmcplugin.endOfDirectory(plugin.handle)




#------------------------------video--------------------------------------

@plugin.route('/get_video/<path:url>')
def get_video(url):
    PROTOCOL = 'mpd'
    DRM = 'com.widevine.alpha'
    source_type = _addon.getSetting('source_type')
    soup = get_page(url)
    desc = soup.find('meta', {'name':'description'})['content'].encode('utf-8')
    #showtitle = ''#soup.find('h2', {'class':'subtitle'}).find('a').get_text().encode('utf-8')
    titleEp = soup.find('h1', {'class':'title'}).get_text().encode('utf-8').strip()
    #print(title)
    #soupTi=soup.find('h1', {'class':'title'})
    if str(url).find('/filmy/')>0 :
        try:
            for span_tag in soup.find('span', {'class':'sub'}):
                span_tag.replace_with('')
            souti=soup.prettify()
            title=soup.find('h1', {'class':'title'}).get_text().encode('utf-8').strip()
        except:
            title=soup.find('h1', {'class':'title'}).get_text().encode('utf-8').strip()
        #print(title)
        imgs = soup.find('div', {'class':'img'})
        #print(imgs)
        try:
            img=imgs.img['data-src']
        except:
            img=imgs.picture.img['src']
        #print(img)
        medtyp='movie'
    else:
        #title=soup.find('h2', {'class':'subtitle'}).get_text().encode('utf-8').strip()
        title=soup.find('h2', {'class':'text'}).get_text().encode('utf-8').strip()
        print('serial')
        print(title)
        #art_url=soup.find('h2', {'class':'subtitle'})
        #url=art_url.a['href']
        #print(url)
        #print(title)
        #imgs = soup.find('a', {'class':'img'})
        #print(imgs)
        #try:
        #    img=imgs.img['data-src']
        #except:
        #    img=imgs.picture.img['src']
        #print(img)
        img='nonexistent'
        medtyp='episode'
    roktime=soup.find_all('time')
    try:
        year=roktime[0]['datetime'][0:4]
    except:
        year=''
    try:
        time=roktime[1]['datetime']
    except:
        time=''    
    try:
        tim=int(''.join(filter(str.isdigit, time)))*60
    except:
        tim=0
    #print(imgs)
    #print(img)
    embeded = get_page(soup.find('div', {'class':'c-player-wrap'}).find('iframe')['src'])
    if str(embeded).count("$.klebetnica"):        
        if str(embeded).count("player_device_limit_reached"):        
            notice = xbmcgui.Dialog()
            registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30104)) #'Presiahli ste povolený počet zariadení'
        elif str(embeded).count("player_not_logged_in"):        
            notice = xbmcgui.Dialog()
            registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30105)) #"Prístup k médiu je neautorizovaný. Skontrolujte, či ste zadali správne prihlasovacie údaje"
        else:
            notice = xbmcgui.Dialog()
            registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30106)) #"Chyba pri prehrávaní, skontrolujte platnosť vášho účtu VOYO"
    else:
        script = embeded.find_all('script')[-1]
        json_data = json.loads(re.compile('{\"tracks\":(.+?),\"duration\"').findall(str(script))[0])
		#print(title, img, url, desc)
        data={'mediatype': medtyp, 'title': title, 'plot' : desc, 'year' : year, 'duration': tim}
#    print(data)
        rec=SqlRun( mode='write', title=title, url=url, url_img=img, data=data)
#    print(rec)



    if json_data:
        print (json_data)
        stream_data = json_data[source_type][0]
        list_item = xbmcgui.ListItem()
        list_item.setInfo('video', {'mediatype': medtyp, 'title': title, 'plot' : desc})
        if not 'drm' in stream_data and source_type == 'HLS':
            list_item.setPath(stream_data['src'])
        else:
            is_helper = inputstreamhelper.Helper(PROTOCOL, drm=DRM)
            if is_helper.check_inputstream():
                stream_data = json_data['DASH'][0]
                print(stream_data['type'])
                list_item.setPath(stream_data['src'])
                list_item.setContentLookup(False)
                list_item.setMimeType('application/xml+dash')
                list_item.setProperty('inputstream', 'inputstream.adaptive')
                list_item.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
                if 'drm' in stream_data:
                    drm = stream_data['drm'][1]
                    list_item.setProperty('inputstream.adaptive.license_type', DRM)
                    list_item.setProperty('inputstream.adaptive.license_key', drm['serverURL'] + '|' + 'X-AxDRM-Message=' + drm['headers'][0]['value'] + '|R{SSM}|')
        xbmcplugin.setResolvedUrl(plugin.handle, True, list_item)
    else:
        xbmcgui.Dialog().notification(_addon.getAddonInfo('name'),_addon.getLocalizedString(30101), xbmcgui.NOTIFICATION_ERROR, 5000)



#------------------------------databáze--------------------------------------


#def data_dir():
#    """"get user data directory of this addon.
#	according to http://wiki.xbmc.org/index.php?title=Add-on_Rules#Requirements_for_scripts_and_plugins
#	"""
#    datapath = translatePath(ADDON.getAddonInfo('profile'))
#    if not xbmcvfs.exists(datapath):
#        xbmcvfs.mkdir(datapath)
#    return datapath

# ukázka kodu, vložení řádků pomocí parametrů
def insertVaribleIntoTable(name, email, joinDate, salary):
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data_Drac.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # zjištění počet záznamů
        sqlite_select_query = """SELECT * from SqliteDb_developers"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print('počet záznamov: ', len(records))
        id=len(records)+1
        print(id)

        #vložení záznamů
        sqlite_insert_with_param = """INSERT INTO SqliteDb_developers
                          (id, name, email, joining_date, salary) 
                          VALUES (?, ?, ?, ?, ?);"""

        data_tuple = (id, name, email, joinDate, salary)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        print("Failed to insert data into sqlite table")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        #exc_type, exc_value, exc_tb = sys.exc_info()
        #print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


# ukázka kodu, výpis všech řádků
def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data_Drac.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from SqliteDb_developers"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print(row)
            print("Id: ", row[0])
            print("Name: ", row[1])
            print("Email: ", row[2])
            print("JoiningDate: ", row[3])
            print("Salary: ", row[4])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

# ukázka kodu, výpis všech řádků
def CreatSqliteTable():
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data_Drac.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        # dotaz na verzy sql tabulky    
        #sqlite_select_Query = "select sqlite_version();"
        #cursor.execute(sqlite_select_Query)
        #record = cursor.fetchall()
        #print("SQLite Database Version is: ", record)
        # vytvoření tabulky SqliteDb_developers
        sqlite_create_table_query = '''CREATE TABLE if not exists SqliteDb_developers (
                                    id INTEGER PRIMARY KEY,
                                    name TEXT NOT NULL,
                                    email text NOT NULL UNIQUE,
                                    joining_date datetime,
                                    salary REAL NOT NULL);'''
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite table created")
        cursor.close()


    except sqlite3.Error as error:
        print("Chybné vytvoření tabulky", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


#vytvoření databáze
def CreatSqlTable():
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data.db')
        cursor = sqliteConnection.cursor()
        print("Připojeno SQLite")

        sqlite_create_table_query = '''CREATE TABLE if not exists Hist_View (
                                    id INTEGER PRIMARY KEY,
                                    title TEXT NOT NULL UNIQUE,
                                    url TEXT NOT NULL,
                                    url_img TEXT NOT NULL,
                                    mediatype text,
                                    plot text,
                                    duration text,
                                    year text,
                                    dataum datetime);'''
        cursor.execute(sqlite_create_table_query)
        sqliteConnection.commit()
        print("SQLite tabulka vytvořena")
        cursor.close()


    except sqlite3.Error as error:
        print("Chybné vytvoření tabulky", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite spojení uzavřeno")

#čtení all databáze
def readSqlData():
    records=None
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data.db')
        cursor = sqliteConnection.cursor()
        print("Připojeno SQLite")

        sqlite_select_query = """SELECT * from Hist_View"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        #print("Total rows are:  ", len(records))
        #print("Printing each row")
        #for row in records:
        #    print(row)
        #    print("Id: ", row[0])
        #    print("title: ", row[1])
        #    print("data: ", row[2])
        #    print("datum: ", row[3])
        #    print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite spojení uzavřeno")
    return records

#zápis hodnot
def insDaSqlTable(title, url, url_img, data):
    ret=None
    try:
        sqliteConnection = sqlite3.connect(_profile+'Data.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # zjištění počet záznamů
        sqlite_select_query = """SELECT * from Hist_View"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print('počet záznamov: ', len(records))
        id=len(records)+1
        print(id)
        print(data)

        #vložení záznamů
        sqlite_insert_with_param = """INSERT INTO Hist_View
                          (id, title, url, url_img, mediatype, plot, duration, year, dataum) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""


        #sqlite_create_table_query = '''CREATE TABLE if not exists Hist_View (
        #                            id INTEGER PRIMARY KEY,
        #                            title TEXT NOT NULL UNIQUE,
        #                            url TEXT NOT NULL,
        #                            url_img TEXT NOT NULL,
        #                            mediatype text,
        #                            plot text,
        #                            duration text,
        #                            year text,
        #                            dataum datetime);'''

        now = datetime.now()
        data_tuple = (id, title, url, url_img, data['mediatype'],  data['plot'],  data['duration'],  data['year'], now)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        print("Failed to insert data into sqlite table")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        #exc_type, exc_value, exc_tb = sys.exc_info()
        #print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
    return ret


#spuštění databáze
@plugin.route('/SqlRunTest/<type>')
def SqlRunTest(type):
    print(_profile)

    CreatSqlTable()

    insertVaribleIntoTable('Joe1', 'joe1@pynative.com', '2019-05-19', 9000)
    insertVaribleIntoTable('Ben2', 'ben2@pynative.com', '2019-02-23', 9500)

    readSqliteTable()


def SqlRun(mode, title, url, url_img, data):
    print(_profile)
    datar=None
    CreatSqlTable()
    now = datetime.now()
    print(now)
    if mode == 'read_all':
        datar=readSqlData()
    if mode == 'write':
        datar=insDaSqlTable(title=title, url=url, url_img=url_img, data=data)

    return datar


#------------------------------Ověření+html--------------------------------------


def get_bpar(b):
    bpar=dict(parse.parse_qsl(parse.urlsplit(b).query))
    return bpar

def get_burl(b):
    burl = parse.urlsplit(b).scheme+'://'+parse.urlsplit(b).netloc+parse.urlsplit(b).path
    return burl

def get_next_page(url, par):
	s = get_session()
	r = s.get(url, headers={'User-Agent': _UserAgent_}, params=par)
	return BeautifulSoup(r.content, 'html.parser')

def get_page(url):
	s = get_session()
	r = s.get(url, headers={'User-Agent': _UserAgent_})
	return BeautifulSoup(r.content, 'html.parser')

def get_session():
	s = requests.session()
	# Load cookies and test auth
	cookie_file = _profile+"cookie"
	cookie_file_exists = os.path.isfile(cookie_file)
	if cookie_file_exists:
		with open(cookie_file, 'rb') as f:
			s.cookies.update(pickle.load(f))
		auth = test_auth(s)
		if auth == 0:
			try:
				os.remove(cookie_file)
			except:
				print ("File not found.")
	else:
		s = make_login(s)
	return s
	
def test_auth(s):
	r = s.get('https://crm.cms.markiza.sk/api/v1/users/login-check', headers={'User-Agent': _UserAgent_})
	try:
		if r.json()['data']['logged_in'] == True:
			auth = 1
	except KeyError:
		auth = 0
	return auth

def make_login(s):
	cookie_file = _profile+"cookie"
	username = xbmcplugin.getSetting(plugin.handle, 'username')
	password = xbmcplugin.getSetting(plugin.handle, 'password')
	data = {
		'email': username,
		'password': password,
		'permanent' : "on",
		'login' : "Prihlásiť",               
		'_do': 'content204-loginForm-form-submit'
	}
	r = s.get('https://voyo.markiza.sk/prihlasenie', headers={'User-Agent': _UserAgent_})
	r = s.post('https://voyo.markiza.sk/prihlasenie', headers={'User-Agent': _UserAgent_}, data=data)
	with open(cookie_file, 'wb') as f:
		pickle.dump(s.cookies, f)
	return s

def performCredentialCheck():
	username = xbmcplugin.getSetting(plugin.handle, 'username')
	password = xbmcplugin.getSetting(plugin.handle, 'password')

	if not username or not password:
		registration_notice = xbmcgui.Dialog()
        registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30107))	#"Na prehrávanie obsahu je potrebný účet na voyo.markiza.sk\n\nAk účet ešte nemáte, zaregistrujte se na voyo.markiza.sk, predplaťte si účet na mesiac alebo rok a v daľšom okne vyplňte prihlasovacie údaje."

		username_prompt = xbmcgui.Dialog()
		usr = username_prompt.input('E-mail')

		if not usr:
			return False
		_addon.setSetting(id='username', value=usr)

		password_prompt = xbmcgui.Dialog()
		pswd = password_prompt.input('Heslo', option=xbmcgui.ALPHANUM_HIDE_INPUT)

		if not pswd:
			return False
		_addon.setSetting(id='password', value=pswd)
		s=get_session()   
		if test_auth(s):        
			registration_notice = xbmcgui.Dialog()
			registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30102)) #'Prihlásenie do služby VOYO prebehlo úspešne.'
		else:
			registration_notice = xbmcgui.Dialog()
			registration_notice.ok(_addon.getAddonInfo('name'), _addon.getLocalizedString(30103)) #'Prihlásenie do služby VOYO nebolo úspešné. Skontrolujte, či ste zadali správne prihlasovacie údaje'
	return True

def  build_url ( dotaz ):
      base_url = sys.argv[ 0 ]
      print(base_url)
      return base_url + '?' + urllib.urlencode(dotaz)

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


#------------------------------root--------------------------------------


@plugin.route('/')
def root():

	try:
		os.mkdir(_profile)
	except OSError:
		print ("Folder already exists.")
	listing = []

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30000)) #'Domov'
	list_item.setArt({'icon': 'DefaultMovies.png'})
	listing.append((plugin.url_for(list_home, 0), list_item, True))	

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30001)) #'Novinky'
	list_item.setArt({'icon': 'DefaultMovies.png'})
	listing.append((plugin.url_for(list_news, 0), list_item, True))	

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30002)) #'Filmy'
	list_item.setArt({'icon': 'DefaultMovies.png'})
	listing.append((plugin.url_for(list_movies, 0), list_item, True))	

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30003)) #'Seriály'
	list_item.setArt({'icon': 'DefaultMovies.png'})
	listing.append((plugin.url_for(list_serials, 0), list_item, True))	

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30004)) #'Relácie'
	list_item.setArt({'icon': 'DefaultTVShows.png'})
	listing.append((plugin.url_for(list_shows, 0), list_item, True))
    
	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30005)) #'Šport'
	list_item.setArt({'icon': 'DefaultTVShows.png'})
	listing.append((plugin.url_for(list_sport, 0), list_item, True))

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30006)) #'Deti'
	list_item.setArt({'icon': 'DefaultVideo.png'})
	listing.append((plugin.url_for(list_kids, 0), list_item, True))

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30008)) #'Hľadat'
	list_item.setArt({'icon': 'DefaultAddonsSearch.png'})
	listing.append((plugin.url_for(list_search, 0), list_item, True))

	list_item = xbmcgui.ListItem(_addon.getLocalizedString(30009)) #'História sledovania'
	list_item.setArt({'icon': 'DefaultAddonsSearch.png'})
	listing.append((plugin.url_for(list_HistView, 0), list_item, True))

	#list_item = xbmcgui.ListItem('testSql')
	#list_item.setArt({'icon': 'DefaultAddonsSearch.png'})
	#listing.append((plugin.url_for(SqlRunTest, 0), list_item, True))


	xbmcplugin.addDirectoryItems(plugin.handle, listing, len(listing))
	xbmcplugin.endOfDirectory(plugin.handle)

def run():
	credentialsAvailable = performCredentialCheck()

	if credentialsAvailable:
		plugin.run()
	else:
		xbmc.executebuiltin("Action(Back,%s)" % xbmcgui.getCurrentWindowId())
		sys.exit(1)
