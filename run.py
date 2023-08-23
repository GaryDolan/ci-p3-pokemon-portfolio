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

# Used to hash passwords
import bcrypt

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
    clear_terminal()

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
        print("3. Password reset\n")

        login_selection = input("Enter your selection: ")

        validated_selection = validate_selection(login_selection, list(range(1, 4)))

        if validated_selection == 1:
            account_login()
            break
        elif validated_selection == 2:
            create_account()
            break
        elif validated_selection == 3:
            reset_password()
            break


def account_login():
    """
    Allows user to login to app using their username and password
    Retrieves stored password for username and compares to entered pass

    Parameters:
        None
    Returns:
        None
    """

    clear_terminal()
    print_art_font("       Account  Login")

    print("\n\n\n")
    print_center_string(
        colored(
            "Please enter your username and password below to login (both are case sensitive)\n",
            attrs=["bold", "underline"],
        )
    )

    username = get_valid_username(False)

    if check_username_in_use(username):
        password_attempt = get_valid_password(False)

        print_center_string("Logging in ....\n")

        # Find the row their username is on and return the corrisponding password
        login_worksheet = SHEET.worksheet("login")
        username_found = login_worksheet.find(username, in_column=1)
        row_num = username_found.row
        stored_hashed_pass = login_worksheet.cell(row_num, 2).value

        # Slice the b'' from the stored pass and change type from string to bytes for comparison
        stored_hashed_pass = stored_hashed_pass[2:-1].encode("utf-8")
        password_attempt_bytes = password_attempt.encode()

        if bcrypt.checkpw(password_attempt_bytes, stored_hashed_pass):
            print_center_string(colored("Login Successful\n", "green"))
            # return true to main menu from this call and then call main menu and create use object
            main_menu()
        else:
            print_center_string(colored("Login failed, password incorrect\n", "red"))

    else:
        print_center_string(
            colored("The username entered is not associated with an acconut\n", "red")
        )

        while True:
            print_center_string(
                colored(
                    "Please select option (1 or 2) from the list shown and enter it below\n",
                    attrs=["bold", "underline"],
                )
            )

            print("1. Proceed to main menu")
            print("2. Return to home page\n")

            login_selection = input("Enter your selection: ")

            validated_selection = validate_selection(login_selection, list(range(1, 3)))

            if validated_selection == 1:
                main_menu()
                break
            elif validated_selection == 2:
                display_welcome_banner()
                break


def create_account():
    """
    Used to create a new user account
    Takes username, password and phone num from user and validates
    Stores new user details in google sheet
    Assigns the user a column in the base_set_shadowless sheet
    Preps workbook for next user

    Parameters:
        None
    Returns:
        None
    """
    clear_terminal()
    print_art_font(" Account Creation")

    print("\n\n\n")
    print_center_string(
        colored(
            "Please follow the steps below to create an account\n",
            attrs=["bold", "underline"],
        )
    )

    # get new user details
    username = get_valid_username()
    print_center_string(colored("Username available\n", "green"))
    password = get_valid_password()
    phone_num = get_valid_phone_num()

    print_center_string("Creating Account ....\n")

    # Store user account details
    account_details = [username, password, phone_num]
    login_worksheet = SHEET.worksheet("login")
    login_worksheet.append_row(account_details)

    # Assign the user the next available column in base_set_shadowless sheet and add his username to column
    bss_worksheet = SHEET.worksheet("base_set_shadowless")
    next_avail_column = bss_worksheet.acell("A2").value
    bss_worksheet.update_acell(next_avail_column + "1", username)

    # Increment the next_avail_column stored in gsheets, and add a new column to ensure were always ready and hava a column for next account creation
    bss_worksheet.update_acell("A2", increment_gsheet_column_value(next_avail_column))
    add_column_to_sheet("base_set_shadowless")

    print_center_string(
        colored("Account created successfully\n", "green", attrs=["bold", "underline"])
    )

    while True:
        print_center_string(
            colored(
                "Please select option (1 or 2) from the list shown and enter it below\n",
                attrs=["bold", "underline"],
            )
        )

        print("1. Create another account")
        print("2. Return to home page\n")

        login_selection = input("Enter your selection: ")

        validated_selection = validate_selection(login_selection, list(range(1, 3)))

        if validated_selection == 1:
            create_account()
            break
        elif validated_selection == 2:
            display_welcome_banner()
            break


def reset_password():
    """
    Allows user to reset password
    """
    clear_terminal()

    print_art_font("      Password  Reset")

    print("\n\n\n")
    print_center_string(
        colored(
            "Please follow the steps below to reset your password\n",
            attrs=["bold", "underline"],
        )
    )

    phone_num = get_valid_phone_num(False)

    print_center_string("Checking for account ....\n")

    if check_phone_num_in_use(phone_num):
        # Find the row their phone number is on and return the corrisponding username
        login_worksheet = SHEET.worksheet("login")
        phone_num_found = login_worksheet.find(phone_num, in_column=3)
        row_num = phone_num_found.row
        username = login_worksheet.cell(row_num, 1).value

        print_center_string(
            colored(f"Account found, username is {username}\n", "green")
        )

        # Get and store new password
        hashed_password = get_valid_password()

        # Write users new hashed pass
        login_worksheet.update_acell("B" + str(row_num), hashed_password)

        print("")
        print_center_string(colored("Password has been reset\n", "green"))

    else:
        print_center_string(
            colored(
                "The phone number entered is not associated with an acconut\n", "red"
            )
        )

    # Return to login menu or try again
    while True:
        print_center_string(
            colored(
                "Please select option (1 or 2) from the list shown and enter it below\n",
                attrs=["bold", "underline"],
            )
        )

        print("1. Reset password again")
        print("2. Return to home page\n")

        login_selection = input("Enter your selection: ")

        validated_selection = validate_selection(login_selection, list(range(1, 3)))

        if validated_selection == 1:
            reset_password()
            break
        elif validated_selection == 2:
            display_welcome_banner()
            break


def main_menu():
    pass


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


def check_username_in_use(username):
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


def check_phone_num_in_use(phone_num):
    """
    Check if phone number is already stored in google sheet

    Parameters:
        username (string): String to search for in gogle sheets
    Returns:
        True or False (boolean): True if username found, false otherwise
    """
    login_worksheet = SHEET.worksheet("login")
    phone_num_found = login_worksheet.find(phone_num, in_column=3)
    if phone_num_found:
        return True
    else:
        return False


def hash_password(password):
    """
    Hashes given password using a generated salt

    Parameters:
        password (string): Password to be hashed
    Returns:
        password (string): String representing the hashed password
    """
    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode(), salt)

    # retured as strings for storage in gsheets
    hashed_pass = str(hashed_pass)

    return hashed_pass


# ----------------------- GSHEETS FUNCTIONS -----------------------


def increment_gsheet_column_value(column):
    """
    Used to increment column values in gsheets.
    Pass in A returns B
    Pass in Z returns AA
    Pass in GZ returns HA etc.

    Parameters:
        column (string): Column to be incremented
    Returns:
        incremented_col (string): Value of the next column

    """
    # use in the case where we reach Z and need to move to AA
    if column == "":
        return "A"

    last_char_in_column = column[-1]
    other_chars = column[:-1]

    if last_char_in_column == "Z":
        # call this function again passing in other_chars to update the letters before the Z and change the Z to A
        return increment_gsheet_column_value(other_chars) + "A"
    else:
        return other_chars + chr(ord(last_char_in_column) + 1)


def add_column_to_sheet(sheet_name):
    """
    Adds a new column to the specified google sheet

    Parameters:
        sheet_name (string): Sheet to add column to
    Returns:
        None:
    """
    worksheet = SHEET.worksheet(sheet_name)
    empty_lists = [[]]
    last_col_index = worksheet.col_count - 1
    worksheet.insert_cols(
        empty_lists,
        col=last_col_index,
        value_input_option="RAW",
        inherit_from_before=True,
    )


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


def get_valid_username(check_for_match=True):
    """
    Gets a valid username from the user
    Username can be between 5-15 chars long and include _ or -

    Parameters:
        check_for_match (boolean): Flag used to control if we check gsheets for matching username
    Returns:
        username (string): Validated username chosen by user

    """
    while True:
        try:
            username = input(
                "\nPlease enter username between 5 and 15 characters long,\n(You may use letters, numbers, _ or -) : "
            )

            if len(username) < 5:
                raise ValueError("Username must be at least 5 characters")

            if len(username) > 15:
                raise ValueError("Username can not be more than 15 characters")

            if not re.match("^[a-zA-Z0-9_-]*$", username):
                raise ValueError("Username can only use letters, numbers, _ or -")

            if check_for_match:
                if check_username_in_use(username):
                    raise ValueError("Username aleady in use")
            return username

        except ValueError as e:
            print("")
            print_center_string(
                colored(f"Invalid username: {e}, please try again\n", "red")
            )


def get_valid_password(hash_pass=True):
    """
    Gets a valid password from user
    Password can be between 5 and 15 chars and use  _ , - , & or !
    Hashes password via call to external function

    Parameters:
        hash_pass: Flag to allow password hashing to be skipped
    Returns:
        password (string): Validated, Hashed password"""
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

            if hash_pass:
                password = hash_password(password)
                return password
            else:
                return password

        except ValueError as e:
            print("")
            print_center_string(
                colored(f"Invalid Password: {e}, please try again\n", "red")
            )


def get_valid_phone_num(check_for_match=True):
    """
    Gets a valid phone number from user
    Phone number can be between 10 and 15 digits

    Parameters:
        check_for_match (boolean): Flag used to control if we check gsheets for matching number
    Returns:
        phone_num (string): Validated phone number chosen by user
    """
    while True:
        try:
            phone_num = input(
                "\nPlease enter your mobile phone number consisting of 10 to 15 digits: "
            )

            if len(phone_num) < 10:
                raise ValueError("Phone number must be at least 10 digits")

            if len(phone_num) > 15:
                raise ValueError("Phone number cannot be more than 15 digits")

            if not re.match("^[0-9]*$", phone_num):
                raise ValueError("Please only use numbers")

            if check_for_match:
                if check_phone_num_in_use(phone_num):
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


# Ensures main is only excuted when the script is directly run
if __name__ == "__main__":
    main()
