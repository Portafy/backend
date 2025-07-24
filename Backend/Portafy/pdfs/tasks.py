from celery import shared_task
from django.core.exceptions import ValidationError
from core.utils import gemini_api
from .utils import extract_text_blocks, PROMPT

@shared_task
def process_pdf(pdf_path):
    """
    Task to process a PDF file, extract its text, and send it to the Gemini API.
    """
    try:
        pdf_text = extract_text_blocks(pdf_path)
        if not pdf_text:
            raise ValidationError("No text found in the PDF.")


        pdf_text = pdf_text.replace("\n", " ").strip()
        response = gemini_api(PROMPT.replace("{pdf text here}", pdf_text))
        if not response:
            raise ValidationError("No response from the Gemini API.")
        return response

    except Exception as e:
        return str(e)