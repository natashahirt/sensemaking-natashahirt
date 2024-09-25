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
# combined in this file. Instead of having a bunch of extra files you could also just
# bring the functions into one big file and it would work fine.
# -----------------------------------------------

from _imports import *

def export_and_analyze_BU_catalog(url=BU_URL):
    
    scraped_df = scrape_pipeline(url)
    export(scraped_df)
    word_count_df = get_frequency_df(scraped_df)
    visualize_frequency_count(word_count_df, n_words=20) # visualize
