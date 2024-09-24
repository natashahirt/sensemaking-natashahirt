# -----------------------------------------------
#  1. Data Acquisition:
# 
#  Objective: Download all the public course 
#  catalog data in raw HTML format from a 
#  university website.
# 
#  Tools/Resources: Extract all the course 
#  catalog data from one of the follow 
#  three universities:
#     Harvard: https://courses.my.harvard.edu
#     BU: https://www.bu.edu/academics/cas/courses
#     NE: https://catalog.northeastern.edu/course-descriptions
# -----------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd

# functions
def scrape_departments(soup):
    """
    function to get all the links to department sites from the sidebar and returns a
    dictionary. This could be useful if someone is interested in parsing only the courses
    from a specific department
    """

    departments = {}
    
    department_links = soup.find_all("a", class_="level_2")

    for link in department_links:
        
        department_url = link.get("href")
        department_title = link.text.strip()

        departments[department_url] = department_title

    return departments

def get_next_page(soup, current_page_number):
    """
    Gets the next page link.
    """

    pagination = soup.find('div', class_='pagination')
        
    if pagination:

        current_page = pagination.find("span", class_="current") # this is the current page <span>
        
        for link in pagination.find_all("a"):
            
            next_page_number = int(link.text.strip())

            if next_page_number == current_page_number + 1:

                next_page_url = link.get("href")
                print(f"Page {next_page_number}: {next_page_url}")

                return next_page_url, next_page_number
        
    return None, None

def scrape_courses_page(soup):

    course_list = soup.find("ul", class_="course-feed")
    page_courses = []

    if course_list:

        courses = course_list.find_all("li")
        
        for course in courses:

            course_link = course.find("a")

            if course_link is not None:

                course_url = course_link.get('href')
                course_title = course_link.get_text(strip=True)
                course_description = course_link.find_next_sibling(string=True)
                if course_description:
                    course_description = course_description.strip()
                else:
                    course_description = "Description not available"
                
                page_courses.append({
                    "Title": course_title,
                    "Description": course_description,
                    "URL": course_url
                })

            else:
                continue
                print(f"Warning: No <a> tag found in this course: {course.get_text(strip=True)}")

    return page_courses
    
def scrape_bu_courses(url, max_pages = None):

    # send GET request to page
    response = requests.get(url)

    # was request successful?
    if response.status_code == 200:
        
        current_page_url = url
        current_page_number = 1
        all_courses = []

        if not max_pages:
            max_pages = 1e20

        while current_page_url and current_page_number < max_pages:

            response = requests.get(current_page_url)
            if response.status_code != 200:
                print("Response failed.")
                break 

            soup = BeautifulSoup(response.text, 'html.parser')

            if not soup:
                break   # invalid

            all_courses.extend(scrape_courses_page(soup))

            current_page_url, current_page_number = get_next_page(soup, current_page_number)
            
            if not current_page_url:
                print("No more pages found.")
                break   # no more pages found

        df = pd.DataFrame(all_courses)

        return df
    
    else:

        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


"""
Run code
"""

url = "https://www.bu.edu/academics/cas/courses"
course_df = scrape_bu_courses(url)
        
for index, row in course_df.iterrows():
    print(f"Row {index}:")
    print(f"Title: {row['Title']}")
    print(f"Description: {row['Description']}")
    print(f"URL: {row['URL']}")
    print("-" * 40)  # Separator for readability