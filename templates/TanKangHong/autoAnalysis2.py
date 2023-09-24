import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_file: str) -> [str]:
    pdf = PdfReader(pdf_file)
    pdf_text = []

    for page in pdf.pages:
        content = page.extract_text()
        pdf_text.append(content)

    return pdf_text

if __name__ == '__main__':
    extracted_text = extract_text_from_pdf('focs-website/templates/TanKangHong/result.pdf')
    graded_A_count = 0

    for text in extracted_text:
        # Use regular expression to find grades within the "A" range
        grades = re.findall(r'\bA[+-]?\b', text)

        # Check if "CEMERLANG TINGGI" is in the text
        if 'CEMERLANG TINGGI' in text:
            graded_A_count += len(grades)

    print("Grade A with CEMERLANG TINGGI:", graded_A_count)
