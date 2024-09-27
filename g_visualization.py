# -----------------------------------------------
#  7. Data Visualization:
#  Objective: Visualize the word frequencies
#  using a visualization library.
# 
#  Tools/Resources: Examples of visualization 
#  libraries D3, Plotly, and Chart.JS.
#     D3, https://d3js.org/
#     Plotly, https://plotly.com/
#     Chart.JS, https://www.chartjs.org/
#     Google Charts, https://developers.google.com/chart/
# -----------------------------------------------

from _imports import *

def visualize_frequency_count(word_count_df, n_words=10):
    """
    Visualizes the top n_words words as a bar chart.
    """
    top_words_df = word_count_df.head(n_words)
    fig = go.Figure([go.Bar(x=top_words_df["Word"], 
                            y=top_words_df["Count"],
                            text=top_words_df["Count"],
                            textposition='auto',)])
    fig.update_layout(yaxis=dict(
                        title='Word count',
                        titlefont_size=16,
                        tickfont_size=14,),
                      xaxis=dict(
                          tickfont_size=14,),
                      )
    fig.show()
    fig.write_image("results/BU catalog most frequent words.png")