""" This is input for <WriteCommonsCreatorpage.py> that actually writes the Creator-page to Wikimedia Commons using the API
See https://pypi.org/project/mwtemplates/ and https://www.mediawiki.org/wiki/API:Edit
"""

# ===============BEGIN TEMPLETE======================
# Lets make a Wikidata driven {{Creator}} template
#creatorTemplate = """{{{{Creator
# | Wikidata          = {wikidata}
# | Option            = {{{{{{1|}}}}}}
#}}}}
#"""

# Lets create new Commons categories
categoryTemplate = """{{{{Wikidata Infobox}}}}

[[Category:Contributors to the album amicorum Jacobus Heyblocq]]
"""

# ==============END TEMPLATE====================
def writeCreatorTemplate(dataframe,rowdict): # input = 1 full row from the Excel sheet, formatted as dict
    # Input = 1 row from Excel file <<jacob-heyblocq-creatortemplates.xlsx>>, as dict
    # Ouput = Commons source code for a Creator page, based on {{Creator}} template

    #creatorText = creatorTemplate.format(
    creatorText = categoryTemplate.format(
    wikidata = rowdict['CreatorWDQ'].strip()
    )
    return creatorText