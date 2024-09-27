# -----------------------------------------------
#  15. Curriculum Breadth:
# 
#  Compare the breadth of topics in the 
#  1996 and 2024 catalogs to assess whether 
#  the curriculum has become more 
#  interdisciplinary or specialized.
# -----------------------------------------------

from _imports import *

def count_interdisciplinary(df):
    interdisciplinary_keywords = ['cross-disciplinary', 'multidisciplinary', 'integrative', 'applied to', 'interdisciplinary']
    df['Description'] = df['Description'].fillna('')
    df['Interdisciplinary'] = df['Description'].apply(lambda x: any(keyword in x for keyword in interdisciplinary_keywords))
    return df

df_1996 = postprocess_csv("results/mit_1996_courses.csv")
df_2024 = postprocess_csv("results/mit_2024_courses.csv")

df_1996 = count_interdisciplinary(df_1996)
df_2024 = count_interdisciplinary(df_2024)

print("1996: ", df_1996["Interdisciplinary"].sum())
print("2024: ", df_2024["Interdisciplinary"].sum())

"""
Results:
1996:  61
2024:  156
"""