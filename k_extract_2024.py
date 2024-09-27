# -----------------------------------------------
#  11. Catalog 2024
# 
#  Extract course data from the current 
#  MIT course catalog. After extracting the 
#  text, create a data model and save the 
#  processed data.
# -----------------------------------------------

from _imports import *

def scrape_directory(soup):
    """
    function to get all the links to department sites from the sidebar and returns a
    dictionary. This could be useful if someone is interested in parsing only the courses
    from a specific department
    """

    departments = {}
    
    bullet_lists = soup.find_all("ul")

    # Loop through each <ul> and its <li> items
    for ul in bullet_lists:
        for li in ul.find_all("li"):
            # Find all <a> tags inside <li>
            links = li.find_all("a")
            
            # For each link, extract the title and href
            for link in links:
                title = link.get_text()  # Extract the title (text) with possible newlines and spaces
                href = link.get("href")  # Extract the href (link)
                href = "https://student.mit.edu/catalog/" + href

                # Clean the title by removing newlines and stripping excessive spaces
                cleaned_title = title.replace("\n", " ").strip()
                cleaned_title = " ".join(cleaned_title.split())  # Ensure there's only one space between words
                
                # Add cleaned title and link to the departments dictionary
                departments[cleaned_title] = href

    return departments

def is_instructor(line):
    # Use a regex to detect the pattern: capital letter + "." + space + capital letter
    instructor_pattern = r'[A-Z]\.\s[A-Z]'
    return re.search(instructor_pattern, line) is not None

def scrape_department(url):

    # Create a list to store the course names and titles
    department_courses = []

    url_root = url.replace(".html","").strip()[:-1]

    for page_letter in "abcdefghijklmnopqrstuvwxyz":
        
        current_page_url = url_root + page_letter + ".html"

        response = requests.get(current_page_url)
        
        if response.status_code != 200:
            print("Complete.")
            return department_courses

        soup = BeautifulSoup(response.text, 'html.parser')
        page_courses = soup.find_all('h3')

        for (i,course) in enumerate(page_courses):

            next_course = page_courses[i + 1] if i + 1 < len(page_courses) else None
            course_content = []
            sibling = course.find_next_sibling()

            # Loop through the siblings until we hit the next h3
            while sibling and sibling != next_course:
                if sibling.name or sibling.strip():  # Check if it's a tag or non-empty text node
                    course_content.append(str(sibling))
                sibling = sibling.next_sibling

            # Extract the course title
            course_title = course.text.strip()
            parts = course_title.split()  # Split the line by spaces to check its structure
            
            current_course = {
                    "Course Number": parts[0],  # First part is the course number
                    "Course Title": " ".join(parts[1:]),  # The rest is the course title
                    "Description": ""
                }
            
            i = 0

            while i < len(course_content):

                content = course_content[i]

                if 'alt="Not offered"' in content:
                    current_course["Offered"] = content.get('title').strip()

                # Get all content until the next h3
                elif 'alt="Undergrad"' in content:
                    current_course["Class Type (U/G)"] = "Undergraduate"
                elif 'alt="Graduate"' in content:
                    current_course["Class Type (U/G)"] = "Graduate"
    
                # Check for Semester
                elif 'alt="Spring"' in content:
                    current_course["Semester"] = "Spring"
                elif 'alt="Summer"' in content:
                    current_course["Semester"] = "Summer"
                elif 'alt="Fall"' in content:
                    current_course["Semester"] = "Fall"
                elif 'alt="IAP"' in content:
                    current_course["Semester"] = "IAP"

                # check for Rest
                elif 'alt="Rest Elec in Sci &amp' in content:
                    current_course["Rest"] = True

                # check for partial lab
                elif 'alt="Partial Lab' in content:
                    current_course["Partial Lab"] = True

                
                
                # Check for Prereq
                elif 'Prereq:' in content:
                    i += 1
                    content = course_content[i]
                    prereq_soup = BeautifulSoup(content, 'html.parser')
                    # Find all text within <a> tags, which represents the prereq courses
                    prereq_links = prereq_soup.find_all('a')
                    # Extract the text from each <a> tag and join them as a list
                    prerequisites = [link.text for link in prereq_links]
                    current_course["Prerequisites"] = ", ".join(prerequisites)

                    while '<br/>' not in content:
                        i += 1
                        content = course_content[i]
                        content_soup = BeautifulSoup(content, 'html.parser')

                        if 'instructor' in content:
                            current_course["Prerequisites"] = current_course["Prerequisites"] + " " + content.strip()

                        elif 'Coreq:' in content:
                            # Find all text within <a> tags, which represents the prereq courses
                            coreq_links = content_soup.find_all('a')
                            # Extract the text from each <a> tag and join them as a list
                            corequisites = [link.text for link in coreq_links]
                            current_course["Corequisites"] = ", ".join(corequisites)

                        else:
                            prereq_links = content_soup.find_all('a')
                            prerequisites = [link.text for link in prereq_links]
                            current_course["Prerequisites"] = current_course["Prerequisites"] + " " + ", ".join(prerequisites)

                # Check for Units
                elif 'Units:' in content:
                    current_course["Credit structure"] = content.replace('Units: ', '').replace('\n', '')

                elif 'Units arranged' in content:
                    current_course["Units"] = "Units arranged"

                # Check for meets with
                elif "(Subject meets with" in content:
                    i += 1
                    content = course_content[i]
                    prereq_soup = BeautifulSoup(content, 'html.parser')
                    # Find all text within <a> tags, which represents the prereq courses
                    prereq_links = prereq_soup.find_all('a')
                    # Extract the text from each <a> tag and join them as a list
                    prerequisites = [link.text for link in prereq_links]
                    current_course["Prerequisites"] = ", ".join(prerequisites)

                # check for lecture time
                elif 'Lecture:' in content:
                    i += 1
                    content = course_content[i].replace("<i>",'').replace("</i>",'').strip()
                    current_course["Lecture"] = content

                    i += 2
                    content = course_content[i]
                    content_soup = BeautifulSoup(content, 'html.parser')
                    room_link = content_soup.find('a')
                    if room_link:
                        room_text = room_link.text
                        current_course["Lecture"] = current_course["Lecture"] + ", " + room_text

                elif 'Recitation:' in content:
                    i += 1
                    content = course_content[i].replace("<i>",'').replace("</i>",'').strip()
                    current_course["Recitation"] = content

                    i += 2
                    content = course_content[i]
                    content_soup = BeautifulSoup(content, 'html.parser')
                    room_link = content_soup.find('a')
                    if room_link:
                        room_text = room_link.text
                        current_course["Recitation"] = current_course["Recitation"] + ", " + room_text

                elif 'Lab:' in content:
                    i += 1
                    content = course_content[i].replace("<i>",'').replace("</i>",'').strip()
                    current_course["Lab"] = content

                    i += 2
                    content = course_content[i]
                    content_soup = BeautifulSoup(content, 'html.parser')
                    room_link = content_soup.find('a')
                    if room_link:
                        room_text = room_link.text
                        current_course["Lab"] = current_course["Lab"] + ", " + room_text

                # Gather description text
                elif is_instructor(content):
                    content = content.replace("<i>","").replace("</i>","").strip()
                    current_course["Instructor"] = content
            
                else:
                    content_soup = BeautifulSoup(content, 'html.parser')
                    # Extract just the text
                    plain_text = content_soup.get_text(separator=' ').replace("\n",'').replace(')', '').replace('(','').strip()
                    current_course["Description"] += plain_text

                i += 1
            
            if current_course.get("Prerequisites") is not None:
                current_course["Prerequisites"].replace(')', '').strip()
            department_courses.append(current_course)
            
    return(department_courses)
    

def get_MIT_course_catalog(url):

    # send GET request to page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    department_dict = scrape_directory(soup)

    all_courses = []

    for department_url in department_dict.values():
        department_courses = scrape_department(department_url)
        all_courses.extend(department_courses)

    return all_courses,department_dict

def get_courses_dict(department_dict):
    courses_dict = {}
    for value in department_dict.keys():
        course_name = value.split("-")
        if len(course_name) > 1:
            course_number = course_name[0].replace("Course ","").strip()
            course_name = course_name[1].strip()
        else:
            course_name = course_name[0]
            if "(" in course_name:
                course_name = course_name.split("(")
                course_number = course_name[1].replace(")","").strip()
                course_name = course_name[0].strip()
            elif course_name == "Special Programs":
                course_number = "SP"
        courses_dict[course_name] = course_number

    return courses_dict
    
courses_data,department_dict = get_MIT_course_catalog(MIT_URL)
courses_dict = get_courses_dict(department_dict)
df_2024 = pd.DataFrame(courses_data)
df_2024.to_csv('results/mit_2024_courses.csv', index=False)