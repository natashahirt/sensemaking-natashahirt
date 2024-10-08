# -----------------------------------------------
#   3. Data Parsing:
# 
#   Objective: Parse course data leveraging
#   HTML elements structure.
# 
#   Tools/Resources: Use resources like the 
#   DOMParser, BeautifulSoup, or Regular Expressions.
#       Beautiful Soup:
#           https://www.crummy.com/software/BeautifulSoup/
#       DOMParser:
#           https://developer.mozilla.org/en-US/docs/Web/API/DOMParser
#       RegEx:
#           https://regexr.com 
#           https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_expressions
# -----------------------------------------------

# the answer to this is in a_pull under scrape_courses_page
# example run (also found in i_pipeline):

from _imports import *

def scrape_pipeline(url):
    """
    Pipeline for scraping data from the course website given the previous exercises
    """
    all_html = combine_all_pages(url)    # b_combine
    all_soup = BeautifulSoup(all_html, 'html.parser') 
    scraped = scrape_courses_page(all_soup) # a_pull
    scraped_df = pd.DataFrame(scraped)

    return scraped_df