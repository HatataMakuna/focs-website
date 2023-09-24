import fitz  # PyMuPDF

# Define grading criteria and approval/denial rules
grading_criteria = {
    "A": {"min_score": 90, "max_score": 100},
    "B": {"min_score": 80, "max_score": 89},
    "C": {"min_score": 70, "max_score": 79},
    "D": {"min_score": 60, "max_score": 69},
    "F": {"min_score": 0, "max_score": 59},
}

approval_rules = {
    "A": "Approved",
    "B": "Approved",
    "C": "Approved",
    "D": "Denied",
    "F": "Denied",
}

# Function to check grade and approval status
def check_grade_and_approval(score):
    for grade, criteria in grading_criteria.items():
        if criteria["min_score"] <= score <= criteria["max_score"]:
            return grade, approval_rules[grade]
    return "N/A", "N/A"

# Function to process a PDF file and check student results
def process_pdf(pdf_file_path):
    extracted_text = ""
    doc = fitz.open(pdf_file_path)

    # Iterate through pages and extract text
    for page_num in range(doc.page_count):
        page = doc[page_num]
        extracted_text += page.get_text()

    doc.close()

    # Process and analyze the extracted text (replace this with your parsing logic)
    # In this simplified example, we assume that each line contains a student name and score.
    lines = extracted_text.split('\n')
    student_results = []
    for line in lines:
        parts = line.split(',')
        if len(parts) == 2:
            name = parts[0].strip()
            score = int(parts[1].strip())
            grade, approval_status = check_grade_and_approval(score)
            student_results.append({"name": name, "score": score, "grade": grade, "status": approval_status})

    return student_results

# Sample PDF file path (replace with user-uploaded file path)
pdf_file_path = "focs-website/templates/TanKangHong/result.pdf"

# Process the PDF file and get student results
results = process_pdf(pdf_file_path)

# Display the results (you can customize this part to your needs)
for result in results:
    print(f"Name: {result['name']}, Score: {result['score']}, Grade: {result['grade']}, Status: {result['status']}")
