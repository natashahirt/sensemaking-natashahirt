# -----------------------------------------------
#  6. Word Frequency Analysis:
# 
#  Objective: Perform a word frequency count 
#  on the course titles.
# 
#  Tools/Resources: You can use a “map reduce” 
#  style word counting approach.
# -----------------------------------------------

from _imports import *

def scrape_pipeline(url):
    
    all_html = combine_all_pages(url)    # b_combine
    all_soup = BeautifulSoup(all_html, 'html.parser') 
    scraped = scrape_courses_page(all_soup) # a_pull
    scraped_df = pd.DataFrame(scraped)

    return scraped_df

def get_frequency_count(url):

    scraped_df = scrape_pipeline(url)

    mapped_titles = scraped_df['Title'].apply(lambda x: x.lower().split()) # convert to lowercase and split into words

    flat_titles = [word for sublist in mapped_titles for word in sublist] # one list of many words
    word_frequencies = Counter(flat_titles)
    word_count_df = pd.DataFrame(word_frequencies.items(), columns=['Word', 'Count'])

    return word_count_df