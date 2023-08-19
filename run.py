# ------------------------- LIBRARY IMPORTS ---------------------------
# Created by me to store and print pokemon ascii art 
from pokemon_ascii_art import print_pokemon
# Creates text-based ASCII art banners
import pyfiglet as pyf


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

# login = SHEET.worksheet('login')

# data = login.get_all_values()
# print(data)

# --------------------------- CLASSES -----------------------------




# -------------------------- FUNCTIONS ----------------------------

def display_welcome_banner():
    font = pyf.Figlet(font="big", width=110)
    welcome_msg = font.renderText("Pokemon Portfolio")
    welcome_msg = welcome_msg.rstrip()

    print(welcome_msg)
    print_pokemon("pikachu_banner")


# ----------------------------- MAIN -------------------------------

def main():
    """
    Run Pokemon Portfolio command-line utility 
    """
    display_welcome_banner()

main()