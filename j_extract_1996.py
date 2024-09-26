# -----------------------------------------------
#  10. Catalog 1996
# 
#  Extract course data from the scanned 
#  1996 MIT course catalog. After extracting 
#  the text, create a data model and save the 
#  processed data. This task emphasizes 
#  working with raw, scanned documents 
#  and aims to teach you how to extract 
#  information from non-digitized sources.
# -----------------------------------------------

from _imports import *

def get_text_from_pdf(pdf_path="assets/1996_catalog.pdf"):
    with fitz.open(pdf_path) as pdf_document:
        text = ""
        for page_num in range(305,577):
            page = pdf_document.load_page(page_num)
            text += page.get_text("text")
    
    lines = text.splitlines()  # Split text into lines
    processed_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # If the line ends with "- ", merge it with the next line
        while line.endswith("- ") and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            line = line[:-2] + next_line  # Remove the hyphen and concatenate with the next line
            i += 1  # Skip the next line since it's merged
        processed_lines.append(line)
        i += 1
    
    text = "\n".join(processed_lines)
    return text
    
def is_instructor(line):
    # Use a regex to detect the pattern: capital letter + "." + space + capital letter
    instructor_pattern = r'[A-Z]\.\s[A-Z]'
    return re.search(instructor_pattern, line) is not None

def parse_courses(text):

    courses = []
    lines = text.splitlines()  # Split text into lines
    current_course = {}
    
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            continue  # Skip empty lines

        # Detect course number (with a period, e.g., 1.107)
        if "Instructor" in current_course or current_course == {}:  # Start search for new if we have an instructor
            parts = line.split()  # Split the line by spaces to check its structure
            if (any(line.startswith(prefix) for prefix in MIT_COURSE_PREFIXES) or line[:1].isdigit()) and '.' in line and len(parts) > 1 and not line.startswith("0") and ',' not in parts[0]:
                # Save previous course before starting new one
                if current_course:
                    current_course["Description"] = re.sub(r"- ", "", current_course["Description"])
                    courses.append(current_course)
                
                # Start new course
                current_course = {
                    "Course Number": parts[0],  # First part is the course number
                    "Course Title": " ".join(parts[1:]),  # The rest is the course title
                    "Description": ""
                }

                # Check if the next line should be appended to the title (use a while loop)
                next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
                while not (next_line.startswith("Prereq.:") or "Units arranged" in next_line or "Same subject as" in next_line or "Subject meets with" in next_line or "Acad" in next_line or "U (" in next_line or "G (" in next_line):
                    current_course["Course Title"] += " " + next_line
                    i += 1  # Skip the next line since it's appended to the title
                    next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""  # Get the next line to check
                    if i + 1 >= len(lines):
                        break  # Prevents index error if there are no more lines
        
        i += 1
        
        if i >= len(lines):
            continue

        line = lines[i].strip()

        # If we have started a course, we expect the rest of the data to follow
        if current_course:
        
            # Detect prerequisites
            if line.startswith("Prereq.:"):
                current_course["Prerequisites"] = line.replace("Prereq.:", "").strip()
                continue
            
            # Detect semester info (U or G for undergraduate/graduate)
            if line.startswith("U (") or line.startswith("G ("):
                parts = line.split()
                current_course["Class Type (U/G)"] = parts[0]
                current_course["Semester"] = parts[1].strip("()")
                continue

            # Detect credit structure
            if '-' in line and line[0].isdigit():
                current_course["Credit Structure"] = line.split()[0]
                current_course["Credit Info"] = " ".join(line.split()[1:])
                continue

            if "Units arranged" in line:
                parts = line.split("Units arranged", 1)
                current_course["Credit Structure"] = "Units arranged"
                current_course["Credit Info"] = parts[1].strip() if len(parts) > 1 else ""
                continue

            # Detect additional class info
            if "(Same subject as " in line:
                line = re.sub(r"Same subject as ", "", line)
                line = re.sub(r"[\[\]\(\)]", "", line)
                current_course["Same subject as"] = line
                continue

            if "(Subject meets with " in line:
                line = re.sub(r"Subject meets with ", "", line)
                line = re.sub(r"[\[\]\(\)]", "", line)
                current_course["Subject meets with"] = line
                continue

            if "Acad" in line:
                line = re.sub(r"[\[\]\(\)]", "", line)
                if current_course.get("Years offered") is None:
                    current_course["Years offered"] = line
                else:
                    current_course["Years offered"] += " " + line
                continue

            # Detect instructor names (we assume names with initials)
            if is_instructor(line):
                # Correction: If "0. " appears in the instructor's name, replace it with "O. "
                if "0" in line:
                    line = line.replace("0", "O")
                current_course["Instructor"] = line
                continue

            # Add remaining lines to the course description
            if "Description" not in current_course:
                current_course["Description"] = line
            else:
                current_course["Description"] += " " + line

    # Add the last course
    if current_course:
        current_course["Description"] = re.sub(r"- ", "", current_course["Description"])
        courses.append(current_course)

    return courses

# Parse the courses
text = get_text_from_pdf()
courses_data = parse_courses(text)
df_1996 = pd.DataFrame(courses_data)
df_1996.to_csv('results/mit_1996_courses.csv', index=False)