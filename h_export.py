# -----------------------------------------------
#  8. Export a Clean Formatted Dataset
#  of the Entire University Catalog:
# 
#  Export a Clean Formatted Dataset of 
#  the Entire University Catalog: The 
#  dataset you would have liked when you 
#  started. Prepare and export a clean, 
#  well-formatted dataset encompassing 
#  the entire university catalog. This 
#  dataset should be in a form that is 
#  readily usable for analysis and 
#  visualization, reflecting the cleaned 
#  and consolidated data you've worked 
#  with throughout the project. Document 
#  the structure of your dataset, including 
#  a description of columns, data types, and 
#  any assumptions or decisions made during 
#  the data preparation process.
# -----------------------------------------------

from _imports import *

def export(df, directory='results/'):

    df.to_csv(directory + "BU_2024_courses.csv", index=False) # export as csv
    records = df.to_dict(orient='records') # export as json
    with open(directory + "scraped_BU_catalog.json", 'w') as f:
        json.dump(records, f, indent=4)