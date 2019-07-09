#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from googletrans import Translator
from lxml import etree
import re
import unicodedata
from django.utils.encoding import smart_str, smart_unicode
from collections import Iterable


from googletrans import Translator  # Import Translator module from googletrans package

translator = Translator() # Create object of Translator.
i = 0 
with open('chs.locale') as fobj:
    xml = fobj.read()

root = etree.fromstring(xml)

for appt in root.getchildren():
    for elem in appt.getchildren():
	if elem.tag == "String":	
		print elem.text
		context = elem.text
		#context = context.decode('utf8').encode('ascii')
		#context = context.encode('ascii')

		#context = re.sub(r"<©®>", "", context)
		have_chinese = False
		    
		if (isinstance(context, Iterable) == False):
			continue
			

		for x in context:
			if re.search(u'[\u4e00-\u9fff]', x):
				#print('found chinese character in ' + x)
				have_chinese = True
				break
	
		if (have_chinese):
			temp_text = (translator.translate(context).text)
			#temp_text = str(translator.translate(context, src='zh-CN', dest='en').text)
			#print (temp_text)	
			elem.text = temp_text
			print elem.text 
			i += 1	#Count number of translation
#		if (i == 2):
#		break
		else:
			print("ignored ... no chinese ...")
		if(i % 30 == 0):	#Will write 30 more translation 
			tree = etree.ElementTree(root)
			tree.write('chs.locale', pretty_print=True, xml_declaration=True, encoding="utf-8")
			print ("rewrite some other...")
		

# serialize the DOM tree and write it to file
tree = etree.ElementTree(root)
tree.write('chs.locale', pretty_print=True, xml_declaration=True, encoding="utf-8")


#print("Hello, We are at the End!")

#testTranslate
#context = "©Alibaba Group 阿里巴巴集团官方出品"
#context = re.sub(r"<©®>", "", context)
#print context
#print(translator.translate(context, dest='en').text)

