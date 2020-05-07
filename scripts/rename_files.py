# Rename jpg and png files

import os.path
import pandas as pd

currentdir = os.path.dirname(os.path.realpath(__file__))  # Path of this .py file
filename = "jacob-heyblocq-wmcommonstitels.xlsx"
excelpath = currentdir + "\\" + filename
sheetname = "wmc-titles-test"
df = pd.read_excel(excelpath, sheet_name=sheetname, header=0)
df.fillna(0, inplace=True) #fill empty cells with 0
dfdict=df.to_dict(orient='records')

imagedir = currentdir + "\\" + "images-wmcnames"
#print(imagedir)

for i in range(0,len(df)):
    source_imagename2 =''
    target_imagename2=''
    print(str(i) + '   aaaaaaaaaa' + '*'*40)
    rowdict = dfdict[i]
    #print(rowdict)

    source_imagename2 = imagedir + "\\" + rowdict['currentfilename']
    source_imagename = source_imagename2.strip()
    print(source_imagename)

    target_imagename2 = imagedir + "\\" + rowdict['targetcommonsfilename'] #Name for WMCommons
    target_imagename = target_imagename2.strip()
    print(target_imagename)

    # Check if target image name is the same at the current source image name : if so, do not rename. If not, then do rename

    if source_imagename == target_imagename:
        print("WMCommons filename IS THE SAME AS current filename, no need to rename")
    else:
        print("WMCommons filename IS BETTER  THAN current filename, we are going to rename!")
        #os.rename(source_imagename, target_imagename)