import subprocess
import sys
import importlib.util

# Required Packages
required = {'colorama', 'tabulate', 'requests'}

def install_missing_packages(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for package in required:
    if importlib.util.find_spec(package) is None:
        print(f"{package} package not installed.")
        user_input = input(f"Would you like to install this package? (Y/N): ").strip().lower()
        if user_input == 'y':
            install_missing_packages(package)
        else:
            print(f"{package} package is not installed. Terminating program.")
            sys.exit(1)

from app_title import print_title
from mail_sender import Mail_Sender as ms
from table import Table
from export_emails import Export_Emails as ee
import time
import os
from key_event import Key_Event as ke
from colorama import Fore, Style, init

init(autoreset=True)

menu_options = ["Extract E-Mail From Website", "Mail Sender", "Exit"]
mail_sender_options = ["Read e-mail addresses from a TXT file","Enter e-mail addresses manually", "Back"]

def print_menu(selected_row_idx, options):
    # ke.save_cursor()
    ke.move_cursor(1, 1)
    print_title()

    select_text = "Select an Option"
    print(f"{Fore.GREEN}{select_text}")

    for idx, option in enumerate(options):
        if idx == selected_row_idx:
            print(f"{Fore.YELLOW}> {option}{' ' * 20}")
        else:
            print(f"  {option}{' ' * 20}")
    # ke.restore_cursor()

def main():
    current_row = 0
    in_mail_sender_menu = False
    
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        ke.hide_cursor()
        directory = "C:/Users/omero/Desktop/company_emails"
        while True:
            current_option = mail_sender_options if in_mail_sender_menu else menu_options
            print_menu(current_row, current_option)
            
            key = ke.get_key()
            if key == '\x1b':  # ESC
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            elif key == 'up' or key == 'w' or key == 'W':
                if current_row > 0:
                    current_row -= 1
            elif key == 'down' or key == 's' or key == 'S':
                if current_row < len(current_option) - 1:
                    current_row += 1
            elif key == ' ' or key == '\r':  # Space or Enter
                if in_mail_sender_menu:
                    if current_row == 0:
                        txt_file_path = os.path.join(directory, "emails.txt")
                        company_emails = ms.get_emails_from_txt(txt_file_path)
                        Table.draw_table(company_emails)
                        ms.confirm_and_send_emails(company_emails)
                    elif current_row == 1:
                        company_emails = ms.enter_email_manually()  
                        Table.draw_table(company_emails)
                        ms.confirm_and_send_emails(company_emails)
                    elif current_row == 2:
                        in_mail_sender_menu = False
                        current_row = 0
                else:
                    if current_row == 0:
                        ee.run_extract()
                    elif current_row == 1:
                        in_mail_sender_menu = True
                        current_row = 0
                    elif current_row == 2:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        sys.exit(0)
            
            time.sleep(0.05)
    except KeyboardInterrupt as e:
        sys.exit(0)
        # pass
    finally:
        ke.show_cursor()
        print(f"{Fore.RED}\nExiting program...")
                
if __name__ == "__main__":
    main()