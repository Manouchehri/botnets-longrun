#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Provides keywords from HTML source
import requests 
import json
import urllib
from alchemyapi import AlchemyAPI

alchemyapi = AlchemyAPI()
# Uses external API to 
def get_keywords(html):
	response = alchemyapi.keywords('html', html, {'sentiment': 1})

	if response['status'] == 'OK':
		keywords = list()
		for k in response['keywords']:
			keywords.append(k['text'])
		return keywords
	return list()
