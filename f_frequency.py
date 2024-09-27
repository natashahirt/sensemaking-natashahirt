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

def split_words(text):
    """
    Split the title string into individual words
    """
    if isinstance(text, float):
        text = str(text)
    words = re.findall(r"\b(?!\d)[\w'-]+\b", text.lower())
    words = filter_words(words)
    return words

def filter_words(words):
    """
    Filter out stopwords (e.g. "in", "and") and digits
    """
    filtered_words = [word for word in words if word.lower() not in STOPWORDS and not re.search(r'\d', word)]  # Remove stopwords
    return filtered_words

def get_frequency_df(df):
    """
    Count the frequency of words and return a dataframe with words and their count
    """
    if "Title" in df:
        mapped_titles = df['Title'].apply(split_words) # convert to lowercase and split into words
    elif "Course Title" in df:
        mapped_titles = df['Course Title'].apply(split_words) # convert to lowercase and split into words
    else:
        print("The title field doesn't exist.")
        return

    flat_titles = [word for sublist in mapped_titles for word in sublist] # one list of many words
    word_frequencies = Counter(flat_titles)
    word_count_df = pd.DataFrame(word_frequencies.items(), columns=['Word', 'Count'])
    word_count_df = word_count_df.sort_values(by='Count', ascending=False)

    return word_count_df