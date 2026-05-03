import gspread
from google.oauth2.service_account import Credentials
import os

def fetch_leads_from_google_sheet():
   

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    SERVICE_ACCOUNT_FILE = os.environ.get(
    "SERVICE_ACCOUNT_FILE",
    "/etc/secrets/service_account.json"   # Render secret path
    )

    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    sheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1Adm1mEb_IzdDZCC05aIREWrQMsnJSEoEQ605X8s-lFk/edit?gid=0#gid=0"
    ).sheet1

    data = sheet.get_all_records()

    filtered_data = []

    for row in data:
        # Get the raw values as strings to avoid errors
        raw_time = str(row.get("created_time", ""))
        raw_phone = str(row.get("phone_number", ""))

        # 1. Trim the Date: Split by 'T' and take the first part
        # "2026-03-17T02:51:28-05:00" -> "2026-03-17"
        clean_date = raw_time.split('T')[0] if 'T' in raw_time else raw_time

        # 2. Trim the Phone: Split by '+91' and take the last part
        # "p:+919630326253" -> "9630326253"
        clean_phone = raw_phone.split('+91')[-1] if '+91' in raw_phone else raw_phone

        filtered_data.append({
            "name": row.get("form_name"),
            "phone": clean_phone,
            "source": row.get("platform"),
            "email": row.get("email"),
            "created_at": clean_date,
        })

    return filtered_data
