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
    word_count_1996 = get_frequency_df(df_1996)
    word_count_2024 = get_frequency_df(df_2024)

    word_count_1996_dict = {row[0]: int(row[1]) for i,row in word_count_1996.iterrows()}
    word_count_2024_dict = {row[0]: int(row[1]) for i,row in word_count_2024.iterrows()}
    all_words = list(set(word_count_1996_dict.keys()).intersection(set(word_count_2024_dict.keys())))

    differences = []

    for word in all_words:
        count_1996 = word_count_1996_dict.get(word, 0)  # Default to 0 if word not found
        count_2024 = word_count_2024_dict.get(word, 0)  # Default to 0 if word not found
        difference = count_2024/len(word_count_2024_dict.keys()) - count_1996/len(word_count_1996_dict.keys())
        differences.append((word, difference))

    # Sort differences by absolute value (largest changes first, positive or negative)
    sorted_differences = sorted(differences, key=lambda x: abs(x[1]), reverse=True)

    # Separate the sorted words and differences into two lists
    words_list = [item[0] for item in sorted_differences][:50]
    differences_list = [item[1] for item in sorted_differences][:50]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=words_list,
        x=differences_list,
        text = words_list,
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
