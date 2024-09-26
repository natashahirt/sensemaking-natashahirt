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

# Note: whoops I overdid it on this one
# -----------------------------------------------

from _imports import *

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
    Gets the next page link using the pagination tab at the bottom of the
    courses container.
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
    """
    Get the courses forom the page. Return a dictionary with headings
    Title // Description // URL
    """

    course_feeds = soup.find_all("ul", class_="course-feed")
    page_courses = []

    for course_feed in course_feeds:

        if course_feed:

            courses = course_feed.find_all("li")
            
            for course in courses:

                course_link = course.find("a")

                if course_link is not None:

                    course_url = course_link.get('href')
                    course_name = course_link.get_text(strip=True)
                    course_number = course_name.split(':', 1)[0].strip()
                    course_title = course_name.split(":", 1)[1].strip()
                    course_description = course_link.find_next_sibling(string=True)
                    if course_description:
                        course_description = course_description.strip()
                    else:
                        course_description = "Description not available"
                    
                    page_courses.append({
                        "Number": course_number,
                        "Title": course_title,
                        "Description": course_description,
                        "URL": course_url
                    })

                else:
                    # it's a hub and not a course
                    pass

    return page_courses
    
def scrape_bu_courses(url, max_pages = MAX_PAGES):
    """
    Using the provided URL, scrape the BU website for the courses and their
    descriptions. Return a dataframe with the scraped information.
    """

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