# Script for https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Voorbeelden#2)_Commons_API

# We request the contributors to the album amicorum (https://commons.wikimedia.org/wiki/Category:Contributors_to_the_album_amicorum_Jacobus_Heyblocq)
# in json format from the API on Wikimedia Commons.
# https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmnamespace=6&gcmtitle=Category:Contributors_to_the_album_amicorum_Jacobus_Heyblocq&format=json
# We only request the File: pages (the images), with gcmnamespace=6.
# We process this json into a basic image thumb gallery ('facebook', Dutch:smoelenboek) in HTML, using the Python script below

######################################################################
import json
import requests
import hashlib
import urllib.parse
from bs4 import BeautifulSoup

# https://stackoverflow.com/questions/33689980/get-thumbnail-image-from-wikimedia-commons
def get_wc_thumb(image, width): # image = e.g. from Wikidata, width in pixels
    image = image.replace(' ', '_') # need to replace spaces with underline
    m = hashlib.md5()
    m.update(image.encode('utf-8'))
    d = m.hexdigest()
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/"+d[0]+'/'+d[0:2]+'/'+image+'/'+str(width)+'px-'+image

######################################################################
HTMLtemplate ="""
<html>
<head>
<!-- # HTML smoelenboek bij https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken/Hergebruik/Voorbeelden#2)_Commons_API
--> 
<meta http-equiv='content-type' content='text/html;charset=utf-8'/>
<link rel="stylesheet" href="./css/bijdragersAAJH-smoelenboek.css"> 
<title>Smoelenboek bijdragers vriendenboek Jacob Heyblocq - Demo o.b.v. Wikimedia Commons API</title>
</head>
<body>
<h1>Smoelenboek bijdragers <a href="https://www.kb.nl/themas/vriendenboeken/verwoede-verzamelaars/jacob-heyblocqs-vriendenboek" 
target="_blank">Vriendenboek Jacob Heyblocq</a> - Demo o.b.v. Wikimedia Commons API</h1>
<ul>
<li>Uitleg & context: <a href="https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken
/Hergebruik/Voorbeelden#2)_Commons_API" target="_blank">https://nl.wikipedia.org/wiki/Wikipedia:GLAM/Koninklijke_Bibliotheek_en_Nationaal_Archief/Topstukken
/Hergebruik/Voorbeelden#2)_Commons_API</a></li>
<li>Zie ook: <a href="https://commons.wikimedia.org/wiki/Category:Contributors_to_the_album_amicorum_Jacobus_Heyblocq" 
target="_blank">https://commons.wikimedia.org/wiki/Category:Contributors_to_the_album_amicorum_Jacobus_Heyblocq</a></li>
</ul>
<div class="fiveColumnGrid">
{gallery}
</div>
</body>
</html>
"""
#######################################
gallery = ""
wmc_baseurl="https://commons.wikimedia.org/wiki/"
wmc_jsonurl = "https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmlimit=500&gcmnamespace=6" \
      "&gcmtitle=Category:Contributors_to_the_album_amicorum_Jacobus_Heyblocq&format=json"

r = requests.get(wmc_jsonurl)
data = json.loads(r.text)
contribs = list(data['query']['pages'].values())
#print(contribs)
for c in contribs:
    contrib = c['title']
    contrib_thumb = urllib.parse.quote(get_wc_thumb(contrib.split("File:")[1], 300)).replace('%3A', ':')
    #Above taken from:  https://stackoverflow.com/questions/1695183/how-to-percent-encode-url-parameters-in-python
    #print(contrib_thumb)
    contrib_link = wmc_baseurl + contrib
    contrib_name = contrib.split("File:")[1].split(".")[0].replace("_", " ")
    gallery += f"<figure class='fiveColumnGridItem'><a target='_blank' href='{contrib_link}'><img src='{contrib_thumb}' alt='{contrib_name}'/></a>" \
               f"<figurecaption><a target='_blank' href='{contrib_link}'>{contrib_name}</a></figurecaption></figure>"

#print(gallery)

html = HTMLtemplate.format(gallery=gallery)
soup = BeautifulSoup(html, 'html.parser')
prettyHTML = soup.prettify()
HTMLoutputfile = open("../bijdragersAAJH-smoelenboek-CommmonsAPI.html", "w")
HTMLoutputfile.write(prettyHTML)
HTMLoutputfile.close()
