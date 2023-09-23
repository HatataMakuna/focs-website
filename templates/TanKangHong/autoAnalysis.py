import pytesseract
from pdf2image import convert_from_path

# Convert the PDF to images
pdf_path = 'C:\\Users\\User\\Downloads\\SEM\\focs-website\\result1.pdf'
images = convert_from_path(pdf_path, first_page=0, last_page=1)

# Check if any pages were converted
if images:
    pdf_image = images[0]  # Assuming you want to work with the first page
    text = pytesseract.image_to_string(pdf_image)

    # Define grade detection criteria
    grade_keywords = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']

    # Detect grades using regular expressions
    detected_grades = [grade for grade in grade_keywords if grade in text]

    # Print the detected grades
    if detected_grades:
        print('Detected Grades:', ', '.join(detected_grades))
    else:
        print('No grades detected.')
else:
    print("No pages found in the PDF.")
