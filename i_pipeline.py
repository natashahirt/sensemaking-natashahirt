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
# -----------------------------------------------

from _imports import *

course_df = scrape_bu_courses(BU_URL)   # a_pull function
all_html = combine_all_pages(BU_URL)    # b_combine function
