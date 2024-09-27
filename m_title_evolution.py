# -----------------------------------------------
#  13. Title Evolution:
# 
#  Conduct a word frequency analysis 
#  on course titles from 1996 and 2024 
#  to explore shifts in academic 
#  terminology and focus areas.
# -----------------------------------------------

from _imports import *

def compare_word_frequencies(df_1996, df_2024):
    word_count_1996 = get_frequency_df(df_1996.head(100))
    word_count_2024 = get_frequency_df(df_2024.head(100))

    word_count_1996_dict = {row[0]: int(row[1]) for i,row in word_count_1996.iterrows()}
    word_count_2024_dict = {row[0]: int(row[1]) for i,row in word_count_2024.iterrows()}
    all_words = list(set(word_count_1996_dict.keys()).intersection(set(word_count_2024_dict.keys())))

    differences = []

    print(word_count_2024_dict["engineering"] - word_count_1996_dict["engineering"])

    for word in all_words:
        difference = word_count_2024_dict[word] - word_count_1996_dict[word]
        differences.append(difference)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=all_words,
        x=differences,
        text = all_words,
        textposition='outside',
        orientation='h',
        marker_color='red'
    ))

    fig.show()

    fig.update_layout(
        title="Word Frequency 1996-2024",
        xaxis_title="Words",
        yaxis_title="Frequency",
        yaxis=dict(
            showticklabels=False,  # Hide y-axis tick labels
            showline=False,  # Hide y-axis line
            showgrid=False   # Hide y-axis gridlines
        ),
        height=2000  # Make the plot taller (increase height)
    )

    fig.update_yaxes(showticklabels=False)
    fig.write_image("results/Title evolution.png")

df_1996 = postprocess_csv("results/mit_1996_courses.csv")
df_2024 = postprocess_csv("results/mit_2024_courses.csv")

compare_word_frequencies(df_1996, df_2024)
