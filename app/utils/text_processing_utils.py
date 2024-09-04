import re


def extract_total_amount(text):
    """
    Extract the total amount from the receipt text.
    Supports INR and USD currencies.
    """
    patterns = [
        # Matches 'Total: 200.00', 'Total - INR 200.00'
        r"Total\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)(?!\s*\d)",
        # Matches 'Grand Total: ₹200.00'
        r"Grand\s*Total\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches 'Total Amount Paid: ₹200.00'
        r"Total\s*Amount\s*Paid\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches under payment summary
        r"PAYMENT SUMMARY.*?\n.*?Credit Card\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches 'Sub Total: ₹200.00'
        r"Sub\s*Total\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches 'Amount Paid: ₹200.00'
        r"Amount\s*Paid\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches 'Net Payable: ₹200.00'
        r"Net\s*Payable\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)",
        # Matches 'Balance Due: ₹200.00'
        r"Balance\s*Due\s*[:\-]?\s*(?:INR|₹)?\s*([\d.,]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            amount = match.group(1).replace(',', '')
            return float(amount)
    return None


def extract_date(text):
    """
    Extract the date from the receipt text.
    Supports multiple date formats.
    """
    patterns = [
        r"Date\s*[:\-]?\s*(\d{2}/\d{2}/\d{2,4})",  # Matches 'Date: 10/07/2024'
        r"Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{2,4})",  # Matches 'Date: 10-07-24'
        r"(\d{2}/\d{2}/\d{2,4})",  # Matches standalone dates '10/07/24'
        r"(\d{2}-\d{2}-\d{2,4})",   # Matches standalone dates '10-07-24'
        r"(\d{4}/\d{2}/\d{2})",  # Matches dates like '2024/07/10'
        r"(\d{4}-\d{2}-\d{2})",   # Matches dates like '2024-07-10'
        r"Date\s*[:\-]?\s*(\w+\s\d{1,2},\s\d{4})"  # Matches 'Date: July 10, 2024'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def extract_merchant_name(text):
    """
    Extract the merchant name from the receipt text.
    Looks for patterns indicating business names and avoids irrelevant lines.
    """
    lines = text.splitlines()

    # Try to find a line that looks like a merchant name, typically near the top
    for line in lines[:10]:  # Inspect the first 10 lines
        line = line.strip()
        if len(line) > 3 and not re.search(r"GST|INR|Date|Total|Bill|No|Token|Qty|Amount|\d", line, re.IGNORECASE):
            if re.search(r"(Ltd|Limited|Store|Retail|Inc|Corporation|Corp|LLC|Shop|Supermarket|Bazaar|Restaurant)", line, re.IGNORECASE):
                return line

    # Fallback: if no clear merchant name found, return the first line that isn't a clear exclusion
    for line in lines:
        line = line.strip()
        if len(line) > 3 and not re.search(r"GST|INR|Date|Total|Bill|No|Token|Qty|Amount|\d|Sub|Grand", line, re.IGNORECASE):
            return line

    return None


def extract_transaction_id(text):
    """
    Extract the transaction or invoice ID from the receipt text.
    """
    patterns = [
        r"Inv\s*No\s*[:\-]?\s*([\w\/\-]+)",  # Matches 'Inv No : HO9907/5/45775'
        r"Invoice\s*No\s*[:\-]?\s*([\w\/\-]+)",
        r"Bill\s*No\s*[:\-]?\s*([\w\/\-]+)",  # Matches 'Bill No : 14644'
        r"Transaction\s*ID\s*[:\-]?\s*([\w\/\-]+)",
        r"Receipt\s*No\s*[:\-]?\s*([\w\/\-]+)",
        r"Bill\s*No\.\s*[:\-]?\s*(\d+)",  # Matches 'Bill No.: 14644'
        # Matches 'Bill No.: 14644' followed by newline or other characters
        r"Bill\s*No\.\s*:\s*(\d+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_payment_method(text):
    """
    Extract the payment method from the receipt text.
    """
    patterns = [
        r"Payment\s*Method\s*[:\-]?\s*(\w+)",  # Matches 'Payment Method: Credit Card'
        r"Paid\s*via\s*[:\-]?\s*(\w+)",  # Matches 'Paid via Card'
        r"Payment\s*Mode\s*[:\-]?\s*(\w+)",
        r"(\w+)\s*Card\s*:\s*[\d.,]+",  # Matches 'Credit Card : 42.00'
        r"Payment\s*Type\s*[:\-]?\s*(\w+)",
        r"Method\s*of\s*Payment\s*[:\-]?\s*(\w+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().title()
    return None


def extract_all_info(text):
    """
    Extract all relevant information from the receipt text.
    """
    return {
        "merchant_name": extract_merchant_name(text),
        "date": extract_date(text),
        "total_amount": extract_total_amount(text),
        "transaction_id": extract_transaction_id(text),
        "payment_method": extract_payment_method(text)
    }
