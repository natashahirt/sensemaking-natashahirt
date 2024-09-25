# -----------------------------------------------
#  9. Data pipeline:
# 
#  Write a program that automates the 
#  sequential execution of previously created 
#  script files, ensuring that each script 
#  runs to completion before the next begins. 
#  This program aims to streamline the 
#  generation of outputs from all your 
#  previous files, consolidating the 
#  results into one sequence.

# NOTE: I used the previous files as sources for my functions which I then
# combined in this file.
# -----------------------------------------------

from _imports import *

def scrape_pipeline(url):
    
    all_html = combine_all_pages(url)    # b_combine
    all_soup = BeautifulSoup(all_html, 'html.parser') 
    scraped = scrape_courses_page(all_soup) # a_pull
    scraped_df = pd.DataFrame(scraped)

    return scraped_df