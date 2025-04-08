
import re
def extract_amount(user_input: str):
    try:
        # Try to convert directly to float (valid number case)
        amount = float(user_input)
        return amount
    except ValueError:
        # Extract numbers and decimal separator from text
        numbers = re.findall(r"\d+[\.,]?\d*", user_input)
        if numbers:
            extracted_number = numbers[0].replace(',', '.')  # Replace comma with dot (if needed)
            try:
                return float(extracted_number)  # Convert to float
            except ValueError:
                return 'error'  # Could not extract a valid number
        else:
            return 'error'

def current_date():
    from datetime import datetime
    from zoneinfo import ZoneInfo
    tashkent_time = datetime.now(ZoneInfo("Asia/Tashkent"))

    current_date = tashkent_time.date()
    return current_date