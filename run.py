# ------------------------- LIBRARY IMPORTS ---------------------------
# Created by me to store and print pokemon ascii art
from pokemon_ascii_art import print_pokemon

# Creates text-based ASCII art banners
import pyfiglet as pyf

# Allows interaction with the operating systems functionalities
import os

# Add colors to text output
from termcolor import colored

# Allows access to functions to work with regular expressions
import re


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
    "https://www.googleapis.com/auth/drive",
]

# Create a Credentials instance from a service account json file
CREDS = Credentials.from_service_account_file("creds.json")

# Create a copy of the credentials with specified scope
SCOPED_CREDS = CREDS.with_scopes(SCOPE)

# Create gspread client using gspread authorize method
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Access sheet for project
SHEET = GSPREAD_CLIENT.open("pokemon_portfolio")

# login = SHEET.worksheet('login')

# data = login.get_all_values()
# print(data)

# --------------------------- CLASSES -----------------------------


# --------------------- APP LOGIC FUNCTIONS -----------------------


def display_welcome_banner():
    """
    Displays welcome banner and image

    Parameters:
        None
    Returns:
        None
    """
    print_art_font("Pokemon Portfolio")

    print_pokemon("pikachu_banner")

    login_options()


def login_options():
    """
    Displays the login opitions to user.
    Takes user selection, validates and calls appropiate function.

    Parameters:
        None
    Returns:
        None
    """
    while True:
        print_center_string(
            colored(
                "Please select an option (1-3) from the list shown and enter it below\n",
                attrs=["bold", "underline"],
            )
        )

        print("1. Log into your account")
        print("2. Create an account")
        print("3. Password recovery\n")

        login_selection = input("Enter your selection:\n")

        validated_selection = validate_selection(login_selection, list(range(1, 4)))

        if validated_selection == 1:
            account_login()
            break
        elif validated_selection == 2:
            create_account()
            break
        elif validated_selection == 3:
            password_recovery()
            break


def account_login():
    clear_terminal()
    print_art_font("        Account Login")
    # print(username is case sensitive)


def create_account():
    clear_terminal()
    print_art_font(" Account Creation")

    print("\n\n\n")
    print_center_string(
        colored(
            "Please follow the steps below to create an account\n",
            attrs=["bold", "underline"],
        )
    )

    username = get_valid_username()
    print_center_string(colored("Username available\n", "green"))

    password = get_valid_password()

    phone_num = get_valid_phone_num()

    print_center_string(colored("Creating Account ....\n", "green"))

    # Store user account details
    account_details = [username, password, phone_num]
    login_worksheet = SHEET.worksheet("login")
    login_worksheet.append_row(account_details)

    print_center_string(
        colored("Accound created successfully\n", "green", attrs=["bold", "underline"])
    )


def password_recovery():
    clear_terminal()
    print_art_font("  Recover Password")


# ----------------------- HELPER FUNCTIONS ------------------------


def print_art_font(string):
    """
    Uses pyfiglet library to convert given string into an art font style

    Parameters:
        text (string): Text to be converted
    Returns:
        None
    """
    font = pyf.Figlet(font="big", width=110)
    msg = font.renderText(string)
    msg = msg.rstrip()
    print(msg)


def print_center_string(string):
    """
    Centers and prints the given text to the terminal
    If text contains ascii escape codes for color etc
    the function will stip these out for calculating
    spacing but will still print original text

    Parameters:
        String (string): String to be centered and printed
    Returns:
        None
    """

    terminal_width = os.get_terminal_size().columns

    # If string contains ascii escape chars, use re to clear them before calculations
    processed_string = re.sub(r"(\x1b|\033)\[[0-9;]*m", "", string)

    spaces = int((terminal_width - len(processed_string)) / 2)
    centered_string = " " * spaces + string
    print(centered_string)


def clear_terminal():
    """
    Clears text from trminal
    """
    if os.name == "posix":  # Linux and macOS
        os.system("clear")
    elif os.name == "nt":  # Windows
        os.system("cls")


def check_username_taken(username):
    """
    Check if username is already stored in google sheet

    Parameters:
        username (string): String to search for in gogle sheets
    Returns:
        True or False (boolean): True if username foun, false otherwise

    """
    login_worksheet = SHEET.worksheet("login")
    username_found = login_worksheet.find(username, in_column=1)
    if username_found:
        return True
    else:
        return False


def check_phone_num_taken(phone_num):
    """
    Check if phone number is already stored in google sheet

    Parameters:
        username (string): String to search for in gogle sheets
    Returns:
        True or False (boolean): True if username foun, false otherwise
    """
    login_worksheet = SHEET.worksheet("login")
    phone_num_found = login_worksheet.find(phone_num, in_column=3)
    if phone_num_found:
        return True
    else:
        return False


# --------------------- VALIDATION FUNCTIONS ----------------------


def validate_selection(selection_str, available_choices):
    """
    Validates user selcection from a choice of numbers
    Validates that it can be converted to an int
    Also validates that user selection was one of the available choices

    Parameters:
        selection_str (string): User selection to be validated
        available_choices (list): List of choices available to user
    Returns:
        int or False: Returns selection value as an int if valid otherwise returns False
    """
    try:
        selection_value = int(selection_str)
        if selection_value not in available_choices:
            raise ValueError(
                f"Available options ({available_choices[0]} - {available_choices[-1]}), you entered {selection_value}"
            )
    except ValueError as e:
        print()
        print_center_string(
            colored(f"Invalid selection: {e}, please try again\n", "red")
        )
        return False
    return selection_value


def get_valid_username():
    while True:
        try:
            username = input(
                "\nPlease enter a username between 5 and 15 characters long,\n(You may use letters, numbers, _ or -) : "
            )

            if len(username) < 5:
                raise ValueError("Username must be at least 5 characters")

            if len(username) > 15:
                raise ValueError("Username can not be more than 15 characters")

            if not re.match("^[a-zA-Z0-9_-]*$", username):
                raise ValueError("Username can only use letters, numbers, _ or -")

            if check_username_taken(username):
                raise ValueError("Username aleady in use")
            return username

        except ValueError as e:
            print("")
            print_center_string(
                colored(f"Invalid username: {e}, please try again\n", "red")
            )


def get_valid_password():
    while True:
        try:
            password = input(
                "\nPlease enter a password between 5 and 15 characters long,\n(You may user letters, numbers, _ , - , & or !) : "
            )

            if len(password) < 5:
                raise ValueError("Password must be at least 5 characters")

            if len(password) > 15:
                raise ValueError("Password cannot be more than 15 characters")

            if not re.match("^[a-zA-Z0-9_&!-]*$", password):
                raise ValueError("Please only use letters, numbers, _ , - , & or !")

            return password

        except ValueError as e:
            print("")
            print_center_string(
                colored(f"Invalid Password: {e}, please try again\n", "red")
            )


def get_valid_phone_num():
    while True:
        try:
            phone_num = input(
                "\nPlease enter a mobile phone number consisting of 10 to 15 digits: "
            )

            if len(phone_num) < 10:
                raise ValueError("Phone number must be at least 10 digits")

            if len(phone_num) > 15:
                raise ValueError("Phone number cannot be more than 15 digits")

            if not re.match("^[0-9]*$", phone_num):
                raise ValueError("Please only use numbers")

            if check_phone_num_taken(phone_num):
                raise ValueError("Phone number aleady in use")

            return phone_num

        except ValueError as e:
            print("")
            print_center_string(
                colored(f"Invalid phone number: {e}, please try again\n", "red")
            )


# ----------------------------- MAIN -------------------------------


def main():
    """
    Run Pokemon Portfolio terminal application
    """
    display_welcome_banner()


main()
