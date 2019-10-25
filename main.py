#!/usr/bin/env python

"""
   _____
  / ____|
 | (___   ___ ___
  \___ \ / __/ _ \
  ____) | (_| (_) |
 |_____/ \___\___/

	Author: Vincent Manzoni
	Copyright:
	Licence:
	Version: 0
	Mail: manzoni.vincent@outlook.fr

	Status: In development
"""

################################################################################
# Imports
################################################################################

import re #for search
import random as rd
import scholarly as sc
import urllib
import pysolr
import json
#import pandas as pd

from solrq import Q
from bs4 import BeautifulSoup

################################################################################
# Functions
################################################################################

##############################
# Print info
##############################

def print_query(query):
	'''Print titles of related query publications
	'''
	print("===================================================================")
	print("=               Infos from ", query)
	print("===================================================================")
	search_query = sc.search_pubs_query(query)
	for i in range(5):
		paper = next(search_query)
		print(paper)

def print_title(query):
	'''Print titles of related query publications
	'''
	print("===================================================================")
	print("=               Titles from ", query)
	print("===================================================================")
	search_query = sc.search_pubs_query(query)
	for i in range(5):
		paper = next(search_query)
		print(paper.bib['title'])

def print_auth_pub(name):
	'''Print titles of the author's publications
	'''
	print("===================================================================")
	print("=               Titles from ", name)
	print("===================================================================")
	search_query = sc.search_author(name)
	author = next(search_query).fill()
	for pub in author.publications:
		print(pub.bib['title'])

def print_abstract(query):
	'''Print abstracts of related query publications
	'''
	print("===================================================================")
	print("=               Abstracts from ", query)
	print("===================================================================")
	search_query = sc.search_pubs_query(query)
	for i in range(5):
		paper = next(search_query)
		print(paper.bib['abstract'])
		print("===================")

##############################
# Get info
##############################

def abstract_from_url(url):
	'''Print abstracts of related url
	'''
	print("===================================================================")
	print("= Abstracts from ", url)
	print("===================================================================")
	data = urllib.request.urlopen(url).read().decode('utf-8')
	data = re.findall(r'<summary[^>]*>([^<]+)</summary>', data)
	abstract = data[0].replace('\n', ' ')
	print(abstract)

def get_p_value(text):
	list = re.findall(r'p[\s]?[=]?[>]?[<]?[\s]?0?[.][0-9]+', text[0])
	if (list):
		print("============P Values=============")
		for i in list:
			print(i)
	return(list)

def get_keyword(text, keywords):
	list = []
	for word in keywords:
		pattern = r"([^.]*?"+word+"[^.]*\.)"
		if (re.findall(pattern, text)):
			list.append(re.findall(pattern, text))
	if (list):
		print("============ Keywords =============")
		for i in list:
			print(i)
	return (list)

def str_to_q(str):
	str = str.replace(" ", "%20")
	str = str.replace("'", "%22")
	return (str)

def api_plos(query):
	'''Print abstracts of related solr query
	'''
	url = "http://api.plos.org/search?q="
	query = str_to_q(query)
	url = url + query
	keywords = ['conclusion', 'results', 'signification', 'conclude',
				'Conclusions', 'findings']
	print("=======================" + "=" * len(url))
	print("= Abstracts from <", url, "> =")
	print("=======================" + "=" * len(url))
	data = urllib.request.urlopen(url).read().decode('utf-8')
#	print(data)
	loaded_json = json.loads(data)
	for paper in loaded_json['response']['docs']:
		print(paper['abstract'][0])
		get_p_value(paper['abstract'])
		get_keyword(paper['abstract'][0], keywords)
		print("=======================" + "=" * len(url))

################################################################################
# Main
################################################################################

def main():
	print("HELLO\n")

#	print_auth_pub('Thibaut Brouillet')
#	print_title('Rubber hand illusion revisited')
#	print_abstract('Rubber hand illusion revisited')
#	print_query('Rubber Hand')
#	abstract_from_url('http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1')
#	print(str_to_q("http://api.plos.org/search?q=abstract:'Rubber Hand Illusion'"))
	api_plos("abstract:'cognitive sciences'")

	print("\nGOODBYE")

if __name__== "__main__":
	main()
