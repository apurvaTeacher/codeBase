import re

def classify_document(text):

    text = text.lower()

    # Invoice keywords
    invoice_keywords = [
        "invoice",
        "invoice number",
        "invoice no",
        "total amount",
        "amount due",
        "bill to",
        "payment due"
    ]

    # Resume keywords
    resume_keywords = [
        "resume",
        "curriculum vitae",
        "work experience",
        "education",
        "skills",
        "professional experience"
    ]

    # Report keywords
    report_keywords = [
        "report",
        "executive summary",
        "findings",
        "conclusion",
        "analysis",
        "recommendation"
    ]

    # Form keywords
    form_keywords = [
        "form",
        "first name",
        "last name",
        "date of birth",
        "signature",
        "address",
        "phone number"
    ]

    if any(keyword in text for keyword in invoice_keywords):
        return "Invoice"

    elif any(keyword in text for keyword in resume_keywords):
        return "Resume"

    elif any(keyword in text for keyword in report_keywords):
        return "Report"

    elif any(keyword in text for keyword in form_keywords):
        return "Form"

    else:
        return "General document"



def extract_metadata(text, category):

    # Email
    email_pattern = r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    emails = re.findall(email_pattern, text)

    # Dates
    date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]+\s+\d{4}|[A-Za-z]+\s+\d{1,2},\s+\d{4})\b'
    dates = re.findall(date_pattern, text)

    # Invoice number
    invoice_pattern = r'(?i)invoice\s*(?:number|no\.?|#)\s*[:\-]?\s*([A-Z0-9\-\/]+)'
    invoice_numbers = re.findall(invoice_pattern, text)

    # Total amount
    amount_pattern = r'(?i)(?:total amount|amount due|grand total|total)\s*[:\-]?\s*(?:INR|USD|EUR|GBP|[$₹€£])?\s*([\d,]+(?:\.\d{1,2})?)'
    total_amounts = re.findall(amount_pattern, text)

    return {
        "emails": emails,
        "dates": dates,
        "invoice_numbers": invoice_numbers,
        "total_amounts": total_amounts
    }


    
    