#TODO : Adapt the code below to create target titles for Wikimedia Commons image upoads for all pages in the Album amicorum of Jacob Heyblocq
# The output must have the following syntax:
# 1- Page: 295
# 2- Current (source) file title : Album Amicorum Jacob Heyblocq - KB131H26_295.jpg
# 3- Target file title for Commons: File:Album amicorum Jacob Heyblocq KB131H26 - p295 - Cornelis van Goor - Drawing of landscape with bridge across river.jpg
# --
# To construct the target WMCommons filename, we need info from the following xml-fields
# 1- <dc:identifier dcx:anchorText="Afbeelding (011)" --> pagenumber as primary key -- DONE
# 2- <dcterms:hasFormat -- DONE
# 3- <dc:title xsi:type="dcx:maintitle" xml:lang="nl"> --- DONE
# 4- <dcx:annotation -- TO DO
# We don't need to extract the contributor name again, this is already stored in an Excel file together with the page number (so we can do a lookup)

import os, os.path
import json
import requests
import re
import urllib
import numpy as np
import pandas as pd
from urllib.request import urlretrieve

# convert SRU-XML to JSON via https://www.oxygenxml.com/xml_json_converter.html
jsonfile="heyblocq-KBcatalogus_05112019-perPagina.json"
with open(jsonfile, encoding="UTF-8") as data_file:
    data = json.load(data_file)

ill_counter = 0  # counts number of illustrations in album
wmc_overall_dict = {}

for i in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
    print('/'*10 + ' Record number ' + str(i) + ' ' + '/'*40) #i=0,1,2,3,4
    wmc_dict = {} #dict per record -- wmc = wikimedia commons
    record = data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][i]["srw:recordData"]["srw_dc:dc"].items() #tuples
    insdict=dict((k, v) for k, v in record)# https://stackoverflow.com/questions/3783530/python-tuple-to-dict
    keys=insdict.keys()
    for key in keys:
        value = insdict[key] #https://realpython.com/python-keyerror/

################Extract data from all <dc:identifier> fields ##############################
    # 1 We only need the page number
    dcid = insdict.get('dc:identifier')
    pagelist = [dcid[j].get('dcx:anchorText').split('(')[1].split(')')[0] for j in range(len(dcid)) if
                 dcid[j].get('dcx:anchorText') != None]  # WOW, most impressive self-written list comprehension!!!
    page = pagelist[0]
    print('Page:' + str(page))

################## Extract data from all dcterms:hasFormat fields
    hasformat=insdict.get('dcterms:hasFormat') #can be None, dict or list of dicts
    if hasformat == None:  #Case 1: No hasformat is provided
        format = 'No format given'
    elif isinstance(hasformat, dict): #Case 2: hasformat is dict (
        format = hasformat.get('content')
    elif isinstance(hasformat, list): #Case 3: Lang is list of dicts (contrib has multiple languages)
        formatlist = [hasformat[i].get('content') for i in range(len(hasformat))]
        format = formatlist
    else: format ="GEEEEN FORMAAATTT"
    print('Format:' + str(format))

################## Extract data from all dc:title fields
    dctitle=insdict.get('dc:title')
    title = dctitle.get('content')
    print('Title:'+str(title))

################## Extract data from all dcx:annotation fields --> <dcx:annotation dcx:label="illustratievermelding">ill</dcx:an
    # Also use this to indicate an illustration via {'dcx:label': 'illustratievermelding', 'content': 'ill'}
    dcxannotation=insdict.get('dcx:annotation')

    #Possible formats for output
    # 1) List, with 1 item and 1 dict
    # -- ['Nederlands gedicht', {'dcx:itemId': '1056116765', 'content': 'Exemplaar met signatuur: Digitaal bestand'}]
    # 2) List, with 2 items and 1 dict
    # -- ['Gedicht op een - uit het album verdwenen - portret van Jacob Heyblocq', 'Afgekeurde versie van het gedicht op p. 94', {'dcx:itemId': '1056115076', 'content': 'Exemplaar met signatuur: Digitaal bestand'}]
    # 3) List with 1 item and 2 dicts
    # -- [{'dcx:label': 'illustratievermelding', 'content': 'ill'}, 'Tekening van de dans van de negen Muzen', {'dcx:itemId': '1056108630', 'content': 'Exemplaar met signatuur: Digitaal bestand'}]
    # 4) List with 2 items and 2 dicts (303
    # -- [{'dcx:label': 'illustratievermelding', 'content': 'ill'}, 'Vgl. p. 289, 291 en 301. Vormen tezamen een citaat uit Propertius: Navita de ventis, de tauris narrat arator // Enumerat miles vulnera, pastor oves', 'Onafgemaakte tekening van een man die os met ploeg voortdrijft (Opschrift: De tauris narrat arator)', {'dcx:itemId': '1056114827', 'content': 'Exemplaar met signatuur: Digitaal bestand'}]
    # 5) Single simple Dict --> This contains non-information, not useful as far as the usability for WMCommons file title goes
    # -- {'dcx:itemId': '1056108630', 'content': 'Exemplaar met signatuur: Digitaal bestand'}
    annolist = []  # list of (cleaned) annotations
    if isinstance(dcxannotation, dict): #Case 5
        annotation = dcxannotation.get('content')
        pass
    elif isinstance(dcxannotation, list): #Cases 1,2,3,4
        for anno in dcxannotation: #anno can be string or dict
            if isinstance(anno, str):  #anno is string
                annolist.append(str(anno))
            elif isinstance(anno, dict):  #anno is dict
                annocontent = anno.get('content') # 'ill'
                annolabel = anno.get('dcx:label') # 'illustratievermelding'
                if annocontent == 'Exemplaar met signatuur: Digitaal bestand':
                    pass
                elif annocontent == 'ill' and annolabel == 'illustratievermelding': #look for illustration
                    annolist.append('Illustration detected')
                    ill_counter += 1
                else:pass
            else:pass
        print('Annotations:'+ str(annolist))
    else:pass # for 'voorplat' and 'achterplat'

    #Fill dicts per record
    wmc_dict['format'] = format
    wmc_dict['title'] = title
    wmc_dict['annotations'] = annolist
    print(str(wmc_dict))

    #Fill overall dict
    wmc_overall_dict[page] = wmc_dict

print(' '*30)
print(' '*30)
print(' '*30)
print('Overall dict:'+ str(wmc_overall_dict))

print(' '*30)
print('Total number of illustrations: ' + str(ill_counter)) #should be 49

# Make Excels of contributors + Check against exsisting 'jacob-heyblocq-bijdragers.xlsx'
# List all contributors, sorted by page number
print(' '*100)
print('Format, title and annotations, sorted by page number:')
#https://stackoverflow.com/questions/9001509/how-can-i-sort-a-dictionary-by-key

dfcolumns = ['page', 'format','title', 'annotations']
df = pd.DataFrame(columns=dfcolumns)

for key in sorted(wmc_overall_dict):
    #print(str(key) + '-' + str(wmc_overall_dict[key]))
    dict = wmc_overall_dict[key]
    page=key
    format = dict.get('format')
    title = dict.get('title')
    annotations = dict.get('annotations')
    wmctuple= (page, format, title, annotations) #naam, gebjaar, sterfjaar, nta, ntaurl, isni, isniurl)
    print(wmctuple)
    #print(list(tuple))
    #https://stackoverflow.com/questions/53500735/appending-a-list-as-dataframe-row
    s = pd.Series(list(wmctuple), index=df.columns)
    df = df.append(s, ignore_index=True)

print(df.head(10))
#df.to_excel("wmctitles.xlsx")
