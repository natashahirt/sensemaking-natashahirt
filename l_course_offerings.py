# -----------------------------------------------
#  12. Course Offerings Over Time
# 
#  After extracting the course data from 
#  both the 1996 and present catalogs, 
#  analyze the number of courses offered 
#  in various departments. Are there any 
#  departments that have significantly 
#  expanded or reduced their course offerings? 
#  If so, identify them and discuss possible 
#  reasons for these changes.
# -----------------------------------------------

from _imports import *

def sort_key(s):
    s = str(s)  # Ensure the element is a string
    # Check if the string is a digit, return an appropriate tuple
    return (0, int(s)) if s.isdigit() else (1, s)

def postprocess_csv(csv_path):
    df = pd.read_csv(csv_path)
    majors = []
    for title in df["Course Number"]:
        course_number = title.split('-')[0]
        if course_number[-1] == ".":
            course_number = course_number[:-1]
        if len(course_number) < 3 or "." not in course_number:
            majors.append(course_number)
            continue
        major, specifier = course_number.split('.')
        if major.isdigit or major in MIT_COURSE_DICT.values():
            majors.append(major)
        elif major in MIT_COURSE_DICT.keys():
            major = MIT_COURSE_DICT[major]
            majors.append(major)

    df["Major"] = majors
    
    return df

def plot_major_frequency(dfs, names, image_title="MIT course offerings 1996 vs 2024"):

    fig = go.Figure()

    for (i,df) in enumerate(dfs):
        course_frequency = {}
        course_frequency = pd.Series(df["Major"]).value_counts()
        course_frequency = course_frequency[course_frequency.index.isin(MIT_COURSE_DICT.values())]
        course_numbers = sorted(course_frequency.index, key=sort_key)
        course_counts = [course_frequency[course].item() for course in course_numbers]  # Maintain order from course_numbers
        fig.add_trace(go.Bar(x=course_numbers, y=course_counts, name=names[i]))
    fig.show()
    fig.write_image("results/" + image_title + ".png")
        
df_1996 = postprocess_csv("results/mit_1996_courses.csv")
df_2024 = postprocess_csv("results/mit_2024_courses.csv")

plot_major_frequency([df_1996,df_2024],["1996","2024"])