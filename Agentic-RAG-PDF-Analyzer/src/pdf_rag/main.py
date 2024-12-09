#!/usr/bin/env python
import sys
import warnings
from pathlib import Path

from crew import PdfRag

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("\nAvailable PDFs in input_pdf directory:")
    pdf_dir = Path(__file__).parent.parent.parent / "input_pdf"
    pdfs = list(pdf_dir.glob("*.pdf"))
    for i, pdf in enumerate(pdfs, 1):
        print(f"{i}. {pdf.name}")
    
    print("\nPress Enter to use the first PDF, or enter the number of the PDF you want to use:")
    pdf_choice = input()
    if pdf_choice.strip():
        try:
            chosen_pdf = pdfs[int(pdf_choice) - 1].name
        except (ValueError, IndexError):
            print("Invalid choice. Using the first PDF.")
            chosen_pdf = pdfs[0].name if pdfs else None
    else:
        chosen_pdf = pdfs[0].name if pdfs else None

    if not chosen_pdf:
        print("No PDF files found in the input_pdf directory!")
        return

    print(f"\nUsing PDF: {chosen_pdf}")
    print("\nEnter your question about the PDF content:")
    user_input = input()

    inputs = {
        'input': user_input,
        'pdf_name': chosen_pdf
    }

    result = PdfRag().crew().kickoff(inputs=inputs)
    print("\nAnswer:", result)

if __name__ == "__main__":
    run()