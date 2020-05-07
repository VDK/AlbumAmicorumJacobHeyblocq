# This is input for <FileUploadToCommons.py> that actually writes the content to Wikimedia commons using the API
#See https://pypi.org/project/mwtemplates/

# ===============BEGIN TEMPLETE======================
# Lets use a minimally filled {{Infomormation}} template - https://commons.wikimedia.org/wiki/Template:Information
fileTemplate = """
=={{{{int:filedesc}}}}==
{{{{Information
 |author             = {author}
 |description        = {{{{en|1=Page {page} of the Album amicorum Jacob Heyblocq KB131H26}}}} 
 |source             = https://resolver.kb.nl/resolve?urn=EuropeanaTravel:131H26:{page}
}}}}

=={{{{int:license-header}}}}==
{{{{Koninklijke Bibliotheek}}}}
{{{{PD-art|PD-old-70-1923}}}}

[[Category:Album amicorum van Jacobus Heyblocq]]
"""

# ==============END TEMPLATE====================
def writeFileTemplate(dataframe,rowdict): # input = 1 full row from the Excel sheet, formatted as dict
    # Input = 1 row from Excel file, as dict
    # Ouput = Commons source code for a file page, based on Information-template

    fileText = fileTemplate.format(
    page = rowdict['page'],
    author = rowdict['contributorname'].strip()
    )
    return fileText