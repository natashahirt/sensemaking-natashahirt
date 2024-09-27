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
    interdisciplinary_keywords = ['cross-disciplinary', 'multidisciplinary', 'integrative', 'for', 'applied to', 'in']
    df['Description'] = df['Description'].fillna('')
    df['Interdisciplinary'] = df['Description'].apply(lambda x: any(keyword in x for keyword in interdisciplinary_keywords))
    return df

df_1996 = postprocess_csv("results/mit_1996_courses.csv")
df_2024 = postprocess_csv("results/mit_2024_courses.csv")

df_1996 = count_interdisciplinary(df_1996)
df_2024 = count_interdisciplinary(df_2024)

print("1996: ", len(df_1996["Interdisciplinary"]))
print("2024: ", len(df_2024["Interdisciplinary"]))

"""
Results:
1996:  2676
2024:  5881
"""