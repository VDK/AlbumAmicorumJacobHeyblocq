import os, os.path
import json
import requests
import re

jsonfile="heyblocq-KBcatalogus_31102019-v2.json"
with open(jsonfile, encoding="UTF-8") as data_file:
    data = json.load(data_file)

for i in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
    print('*'*40+str(i)) #i=0,1,2,3,4
    record = data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][i]["srw:recordData"]["srw_dc:dc"].items() #tuples
    insdict=dict((k, v) for k, v in record)# https://stackoverflow.com/questions/3783530/python-tuple-to-dict
    #print(insdict)
    keys=insdict.keys()
    for key in keys:
        value = insdict[key] #https://realpython.com/python-keyerror/
        #print(str(key) + ":" + str(value))

###creator of contribution
    creatorlist=[]
    creator = insdict.get('dc:creator')
    if creator == None:
       print('creator:Geen')


    elif isinstance(creator, str): #creator is string
        creatorlist.append(str(creator))
        print('creator1:' + str(creatorlist))
        #TODO: Reverse first and last name

    elif isinstance(creator, list):  # creator is list
        print('creatorrrr2:' + str(creator))
        #creator2 = [" ".join(n.split(", ")[::-1]) for n in creator]
        #print('creator2:' + str(creator2)) #https://www.geeksforgeeks.org/print-lists-in-python-4-different-ways/
        #TODO: Reverse first and last name -- http://stackoverflow.com/questions/15704943/switch-lastname-firstname-to-firstname-lastname-inside-list




    elif isinstance(creator, dict):  # creator is dict
        creatorlist.append(str(str(creator['content']).split(' (ISNI')[0]))
        print('creator3:' + str(creatorlist))
        if 'ISNI 'in str(creator['content']):
            creator_isni = creator['content'].split(' (ISNI')[1].split(')')[0]
            print('creator_isni:'+ str(creator_isni))

 ###stuff for scanned contributions
    dcid=insdict.get('dc:identifier')
    #print(dcid)
    dcidlist1 = [(x['xsi:type'], x['content']) for x in dcid]
    #print("aaa" + str(dcidlist1))
    imagageurllist=[]
    for tuple in dcidlist1:
        if 'PPN' in str(tuple[1]):
            print('kbcatlink:' + str(tuple[1]))
        if str(tuple[0]) == 'OCLC':
            print('OCLC-id:' + str(tuple[1]))
        if 'Travel' in str(tuple[1]):
            imagageurllist.append(tuple[1])
    print('imageurls:' + str(imagageurllist))

    ###find page numbers
    dcidlist2 = [dcid[i].get('dcx:anchorText').split('(')[1].split(')')[0] for i in range(len(dcid)) if dcid[i].get('dcx:anchorText') != None] # WOW, most impressive self-written
            # list comprehension!!!
    print('pages:' + str(dcidlist2))

####date of contribution
    date=insdict.get('dc:date')
    date2 = re.sub(r'[\[\]]', '', str(date)) #https://stackoverflow.com/questions/44528081/remove-square-brackets-from-a-list-of-characters
    print('date:'+str(date2))

####lanuage of contribution - NEED WORK
    language=insdict.get('dc:language')
    #print('language:'+str(language))

print('='*100)
print('='*100)

#     #============================================================================
#
#     ppn_long = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][i], "dcx:recordIdentifier")#PRB01:175094691
#     ppn = ppn_long.split(":")[1]#175094691
#
#     title = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dc:title")
 #   date = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][i],"dc:date")
 #   print(data)
#     objectholder = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:recordRights") #in welke collectie zit het boek?
#     booksize = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book], "dcterms:extent")
#
#     thumbnail=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:thumbnail")
#     thumb_url=thumbnail['content']        #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X&role=thumbnail
#     thumb_baseurl=thumb_url.split("&")[0] #http://resolver.kb.nl/resolve?urn=urn:gvn:PRB01:6333948X
#
#     contributorlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:contributor")
#     auteurlist=[]
#     auteurstring=""
#     drukkerlist=[]
#     drukkerstring=""
#     uitgeverlist=[]
#     uitgeverstring=""
#     if str(contributorlist) != "None":
#         if isinstance(contributorlist, dict): # contributorlist = dict
#             if contributorlist['dcx:role'] == "uitgever":
#                 #switch around lastname and firstname of drukker, uitgever, author - see http://stackoverflow.com/questions/15704943/switch-lastname-firstname-to-firstname-lastname-inside-list
#                 uitgeverstring=" / ".join(contributorlist['content'].split(": ")[::-1])
#             elif contributorlist['dcx:role'] == "drukker":
#                 drukkerstring=" / ".join(contributorlist['content'].split(": ")[::-1])
#             elif contributorlist['dcx:role'] == "auteur":
#                 auteurstring=" / ".join(contributorlist['content'].split(": ")[::-1])
#             else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")
#
#         else: # contributorlist = list of dicts
#             for dic in contributorlist:
#                 if dic['dcx:role'] == "uitgever":
#                     uitgeverlist.append(dic['content'])
#                     #switch around lastname and firstname of drukker, uitgever, authors - see http://stackoverflow.com/questions/15704943/switch-lastname-firstname-to-firstname-lastname-inside-list
#                     uitgeverlist2=[" / ".join(uitgever.split(": ")[::-1]) for uitgever in uitgeverlist]
#                 elif dic['dcx:role'] == "drukker":
#                     drukkerlist.append(dic['content'])
#                     drukkerlist2=[" / ".join(drukker.split(": ")[::-1]) for drukker in drukkerlist]
#                 elif dic['dcx:role'] == "auteur":
#                     auteurlist.append(dic['content'])
#                     auteurlist2=[" ".join(auteur.split(", ")[::-1]) for auteur in auteurlist]
#                 else: print("AAaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAAAAAA")
#             uitgeverstring='; '.join(map(str, uitgeverlist2))
#             drukkerstring='; '.join(map(str, drukkerlist2))
#             auteurstring='; '.join(map(str, auteurlist2))
#             #print(str(auteurstring))
#
#     taglist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:subject")
#     tagstring = ""
#     #taglist can either be a string or a list[] of strings
#     #http://www.decalage.info/en/python/print_list
#     if str(taglist) != "None":
#         if isinstance(taglist, str): #taglist is een string
#             tagstring=str(taglist)
#         else: #taglist is een list[] of strings
#             tagstring=', '.join(map(str, taglist))
#
#     alternativelist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:alternative")
#     alternativestring = ""
#     if str(alternativelist) != "None":
#         if isinstance(alternativelist, str):
#             alternativestring=str(alternativelist)
#         else:
#             alternativestring=' '.join(map(str, alternativelist))
#
#     descriptionlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:description")
#     descriptionstring = ""
#     if str(descriptionlist) != "None":
#         if isinstance(descriptionlist, str):
#             descriptionstring=str(descriptionlist)
#         else:
#             descriptionstring=' -- '.join(map(str, descriptionlist))
#
#     annotationlist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcx:annotation")
#     annotationstring = ""
#     if str(annotationlist) != "None":
#         if isinstance(annotationlist, str):
#             annotationstring=str(annotationlist)
#         else:
#             annotationstring='</li><li>'.join(map(str, annotationlist))
#
#     identifier=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dc:identifier")
#     GvNwebsiteURL=[]
#     dci_list=[d['content'] for d in identifier]
#     for item in dci_list:
#         if str(item).startswith("http"):
#             GvNwebsiteURL.append(item)
#
#     ispartoflist=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][book],"dcterms:isPartOf")
#     thisParentID=""
#     for dic in ispartoflist:
#         if dic['xsi:type'] == "parent":
#             thisParentID=str(dic['content'])
#
#     #============================================================================
#
#     file=str(ppn)+".html"
#     HTMLoutputfile = open(str(ppn)+".html", "w")
#     HTMLoutputfile.write("<!DOCTYPE HTML PUBLIC '-//W3C//DTD HTML 4.0//EN' 'http://www.w3.org/TR/REC-html40/strict.dtd'>")
#     HTMLoutputfile.write("<html>")
#     HTMLoutputfile.write("<head>")
#     HTMLoutputfile.write("<title>Beelden voor GVN:PRB01 -- PPN=" +ppn+"</title>")
#     HTMLoutputfile.write("<meta http-equiv='content-type' content='text/html;charset=utf-8'/>")
#     HTMLoutputfile.write("<link href='../lightbox/dist/css/lightbox.css' rel='stylesheet'>")
#     HTMLoutputfile.write("</head>")
#     HTMLoutputfile.write("<body>")
#     HTMLoutputfile.write("<a href='../index.html'><< Terug naar overzichtspagina</a></style>")
#     HTMLoutputfile.write("<h1>Collectie GVN:PRB01 -- PPN= "+ppn+"</h1>")
#     HTMLoutputfile.write("<img src='"+thumb_url+"' align='left' vspace='0' hspace='10'/>")
#     HTMLoutputfile.write("<h2>"+str(title)+"</h2>")
#
#     if alternativestring:
#         HTMLoutputfile.write("<b>Alternatieve titel(s):</b> "+alternativestring+"<br/><br/>")
#
#     HTMLoutputfile.write("<b>Jaar van uitgave:</b> "+str(date)+"<br/><br/>")
#
#     if auteurstring:
#         HTMLoutputfile.write("<b>Auteur(s):</b> "+auteurstring+"<br/>")
#     if uitgeverstring:
#         HTMLoutputfile.write("<b>Naam / plaats uitgever(s):</b> "+uitgeverstring+"<br/>")
#     if drukkerstring:
#         HTMLoutputfile.write("<b>Naam / plaats drukker(s):</b> "+drukkerstring+"<br/>")
#
#     if descriptionstring:
#         HTMLoutputfile.write("<br/><b>Beschrijving:</b> "+descriptionstring+"<br/><br/>")
#     if booksize:
#         HTMLoutputfile.write("<b>Afmetingen:</b> "+booksize+"<br/>")
#     if annotationstring:
#         HTMLoutputfile.write("<b>Opmerkingen:</b><ul><li> "+annotationstring+"</li></ul>")
#     if tagstring:
#         HTMLoutputfile.write("<b>Tags:</b> "+tagstring+"<br/><br/>")
#
#     HTMLoutputfile.write("Dit boek is onderdeel van de collectie van de "+str(objectholder)+"</br/><br/>")
#     HTMLoutputfile.write("Boek op het GvN: <a href='"+GvNwebsiteURL[0]+"'>"+GvNwebsiteURL[0]+"</a><br/>")
#     HTMLoutputfile.write("Beschrijving boek in de KB-catalogus: <a href='http://opc4.kb.nl/PPN?PPN="+ppn+"'>http://opc4.kb.nl/PPN?PPN="+ppn+"</a><br/><br/>")
#
#     rowwidth=5
#     maximages=100
#     numberofimages =0
#     for i in range(0,int(maximages/rowwidth)+1):
#         for j in range(1,rowwidth+1):
#             r = requests.head(thumb_url+"&count="+str(rowwidth*i+j)+"&role=page")
#             if int(r.status_code) == 200:
#                 HTMLoutputfile.write("<a data-lightbox='"+ppn+"' href='"+thumb_baseurl+"&role=page&count=" + str(rowwidth*i+j) + "&role=image&size=large'><img src='"+thumb_url+"&count="+str(rowwidth*i+j)+"&role=page'/></a>")
#                 numberofimages=numberofimages+1
#     HTMLoutputfile.write("<br/><br/>")
#     HTMLoutputfile.write("Aantal beelden = "+  str(numberofimages) +"<br/><br/>")
#
#     #find related books based on same parentID
#     if thisParentID:
#         boekstring="<ol>"
#         teller=0
#         for boek in range(len(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"])):
#             ispartoflist2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek],"dcterms:isPartOf")
#             #print(ispartoflist2)
#             parentID=""
#             for dic2 in ispartoflist2:
#                 if dic2['xsi:type'] == "parent":
#                     parentID=str(dic2['content'])
#             if parentID == thisParentID:
#                 ppn_lang = finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek], "dcx:recordIdentifier")#PRB01:175094691
#                 ppn2=ppn_lang.split(":")[1]#175094691
#                 title2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek], "dc:title")
#                 thumbnail2=finditem(data["srw:searchRetrieveResponse"]["srw:records"]["srw:record"][boek],"dcx:thumbnail")
#                 thumb_url2=thumbnail2['content']
#                 boekstring = boekstring + "<li><img src='"+thumb_url2+"' width='50' align='center'/>&nbsp;&nbsp;<a href='"+ppn2+".html'>"+title2.split(" / ")[0]+"</a><br/><br/></li>"
#                 teller=teller+1
#         HTMLoutputfile.write("<b>Alle "+str(teller)+" boeken in de serie "+thisParentID+":</b>"+boekstring+"</ol>")
#
#     HTMLoutputfile.write("<script src='../lightbox/dist/js/lightbox-plus-jquery.js'></script>")
#     HTMLoutputfile.write("</body>")
#     HTMLoutputfile.write("</html>")
#     HTMLoutputfile.close()
#
#     #make html code beautiful // indent and stuff
#     inputfile = open(file, "r")
#     soup = BeautifulSoup(inputfile, 'html.parser')
#     inputfile.close()
#     outputfile = open(file, "w")
#     outputfile.write(soup.prettify())
#     outputfile.close()

