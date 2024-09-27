# -----------------------------------------------
#  14. New and Discontinued Subjects:
# 
#  Identify subjects that were offered in 
#  1996 but no longer exist in 2024, as 
#  well as new subjects introduced in 2024. 
#  Explore possible reasons for these changes.
# -----------------------------------------------

from _imports import *

def get_unique_subjects():

    df_1996 = postprocess_csv("results/mit_1996_courses.csv")
    df_2024 = postprocess_csv("results/mit_2024_courses.csv")

    courses_only_2024 = set(df_2024["Course Number"]) - set(df_1996["Course Number"])
    courses_only_1996 = set(df_1996["Course Number"]) - set(df_2024["Course Number"])

    df_old = df_1996[df_1996['Course Number'].isin(courses_only_1996)]
    df_new = df_2024[df_2024['Course Number'].isin(courses_only_2024)]
    
    plot_major_frequency([df_old,df_new], ["Old","New"], image_title = "New vs Old")

get_unique_subjects()