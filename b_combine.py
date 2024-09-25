# -----------------------------------------------
#  2. Data Preparation:
# 
#  Objective: Combine multiple HTML files into 
#  a single document.
# 
#  Tools/Resources: Concatenate HTML text using 
#  python or javascript.
# -----------------------------------------------

from _imports import *

def get_page_content(url):

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <ul> with class 'course-feed' (assuming this contains the relevant content)
        page_html = soup.find('ul', class_='course-feed')

        # Return the content if it exists
        if page_html:
            return str(page_html)  # Convert the course feed HTML to a string to concatenate later
        else:
            print("No course feed found on the page.")
            return ""
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return ""
    
def combine_all_pages(url, max_pages = None):

    # send GET request to page
    response = requests.get(url)

    # was request successful?
    if response.status_code == 200:
        
        current_page_url = url
        current_page_number = 1
        all_html = ""

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

            page_content = get_page_content(current_page_url)
            all_html += page_content

            current_page_url, current_page_number = get_next_page(soup, current_page_number)
            
            if not current_page_url:
                print("No more pages found.")
                break   # no more pages found

        return all_html
    
    else:

        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None
    
"""
Run code
"""

all_html = combine_all_pages(BU_URL)