#https://www.mediawiki.org/wiki/API_talk:Upload#Python_with_requests --> this is about page *creation*
#https://www.mediawiki.org/wiki/API:Edit/Editing_with_Python --> this is about page *modification*

# The following code is PD-self & CC-zero
import requests
import os.path
import pandas as pd
import FillFileTemplate
from pathlib import Path

currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file
parentdir=Path(currentdir).parent #Parent folder path, see https://stackoverflow.com/questions/2860153/how-do-i-get-the-parent-directory-in-python
exceldir="excels"
imagedir="images"
excelfile = "jacob-heyblocq-wmcommonstitels.xlsx"
excelpath = str(parentdir) + "\\" + str(exceldir) + "\\" + str(excelfile)
imagepath = str(parentdir) + "\\" + str(imagedir)

sheetname = "wmc-titles"
df = pd.read_excel(excelpath, sheet_name=sheetname, header=0)
df.fillna(0, inplace=True) #fill empty cells with 0
dfdict=df.to_dict(orient='records')



api_url = 'https://commons.wikimedia.org/w/api.php'
#api_url = 'https://commons.wikimedia.beta.wmflabs.org/w/api.php'

# https://www.mediawiki.org/wiki/Special:BotPasswords/OlafJanssenBot
#The bot password for bot name "OlafJanssenBot" of user "OlafJanssen" was updated.
#The new password to log in with OlafJanssen@OlafJanssenBot is <<yourBotpassword>>. Please record this for future reference.
#(For old bots which require the login name to be the same as the eventual username, you can also use OlafJanssen as username and OlafJanssenBot@<<yourBotpassword>> as password.)

#Ensure bot instance is permissioned for createeditmovepage, uploadfile, uploadeditmovefile
USER=u'OlafJanssen@OlafJanssenBot'
PASS=u'<<yourBotpassword>>'
USER_AGENT='OlafJanssenBot'
headers={'User-Agent': USER_AGENT}

# get login token and log in
payload = {'action': 'query', 'format': 'json', 'utf8': '', 'meta': 'tokens', 'type': 'login'}
r1 = requests.post(api_url, data=payload)
#print(r1)
login_token=r1.json()['query']['tokens']['logintoken']
login_payload = {'action': 'login', 'format': 'json', 'utf8': '','lgname': USER, 'lgpassword': PASS, 'lgtoken': login_token}
#print(login_payload)
r2 = requests.post(api_url, data=login_payload, cookies=r1.cookies)
cookies=r2.cookies.copy()
#print(cookies)
# We have now logged in and can request edit tokens thusly:
def get_edit_token(cookies):
        edit_token_response=requests.post(api_url, data={'action': 'query',
                                                    'format': 'json',
                                                    'meta': 'tokens'}, cookies=cookies)
        return edit_token_response.json()['query']['tokens']['csrftoken']


#This is the actual content of the file
# We make two pieces:
# 1) for File image upload = making a new file page
# 2) For file content editing = modifying an existing file page

############# 1) For File Image UPLOAD
#https://www.mediawiki.org/wiki/API_talk:Upload#Python_with_requests --> this is about page *creation*

for i in range(237,239):
#for i in range(0,len(df)):
    rowdict = dfdict[i]
    print(rowdict)
    LOCALFILENAME =  imagepath + "\\" + rowdict['currentfilename'].strip()
    print('LOCALFILENAME = ' + LOCALFILENAME)
    COMMONSNAME= rowdict['targetcommonsfilename'].strip()
    print('COMMONSNAME = ' + COMMONSNAME)
    UPLOADTEXT = FillFileTemplate.writeFileTemplate(df,rowdict)
    print('UPLOADTEXT = ' + UPLOADTEXT)
    UPLOADCOMMENT = 'Creating new image "' + COMMONSNAME + '" via API upload'
    print('UPLOADCOMMENT = ' + UPLOADCOMMENT)
    print("=" * 140)

    #Now actually perform the upload:
    upload_payload={'action': 'upload',
            'format':'json',
            'filename':COMMONSNAME,
            'comment':UPLOADCOMMENT,
            'text':UPLOADTEXT,
            'token':get_edit_token(cookies),
            "ignorewarnings": 1}
    files={'file': (COMMONSNAME, open(LOCALFILENAME,'rb'), 'multipart/form-data')}

    upload_response=requests.post(api_url, data=upload_payload,files=files,cookies=cookies,headers=headers)
    uploaddata = upload_response.json()
    print(uploaddata)
