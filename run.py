# Write for a Terminal of 80 characters wide and 24 rows high


# ---------------------------- API SETUP ------------------------------

# Import the entire gspread library -
# - access to all classes, methods and functions
import gspread

# Import Credentials class from the service account function -
# - part of the google oauth library
from google.oauth2.service_account import Credentials

# Specify what parts of the google account the user has access to
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Create a Credentials instance from a service account json file
CREDS = Credentials.from_service_account_file('creds.json')

# Create a copy of the credentials with specified scope
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Create gspread client using gspread authorize method
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Access sheet for project
SHEET = GSPREAD_CLIENT.open('pokemon_portfolio')

login = SHEET.worksheet('login')

data = login.get_all_values()
print(data)