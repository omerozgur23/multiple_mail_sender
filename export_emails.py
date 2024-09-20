import requests
from bs4 import BeautifulSoup
import re
import os
from key_event import Key_Event as ke
from colorama import Fore, init

init(autoreset=True)

class Export_Emails:

    @staticmethod
    def extract_emails(url):
        try:
            # Pull Web Page
            response = requests.get(url)
            response.raise_for_status()  # Check HHTP Errors

            # Parse HTML Content
            soup = BeautifulSoup(response.text, 'html.parser')

            email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
            emails = set(re.findall(email_pattern, soup.get_text()))
            return emails
        except requests.RequestException as e:
            print(f'{Fore.RED}Error fetching {Fore.YELLOW}{url}: {e}')
            return set()
        
    @staticmethod
    def save_emails_to_file(url, emails, directory, filename):
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_path = os.path.join(directory, filename)
        with open(file_path, 'a') as file:  # Add email addresses by opening in 'a' mode
            for email in emails:
                file.write(email + '\n')
        print(f"{Fore.GREEN}Emails have been saved from: {Fore.YELLOW}{url}")

    @staticmethod
    def save_failed_urls(urls, directory, filename):
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        file_path = os.path.join(directory, filename)
        with open(file_path, 'a') as file:  # Add URLs by opening in 'a' mode
            for url in urls:
                file.write(url + '\n')
        print(f"{Fore.RED}Failed URLs have been saved from: {Fore.YELLOW}{url}")

    def run_extract():
        directory = "C:\\Users\\omero\\Desktop\\company_emails"
        websites_file = os.path.join(directory, "websites.txt")
        emails_file = os.path.join(directory, "emails.txt")
        failed_urls_file = os.path.join(directory, "failed_urls.txt")
        scanned_websites_file = os.path.join(directory, "scanned_websites.txt")
        
        successful_urls = []
        failed_urls = []
        try:
            if not os.path.exists(websites_file):
                print(f"{Fore.RED}{websites_file} not found.")
            else:
                with open(websites_file, 'r') as file:
                    urls = [line.strip() for line in file]
                
                for url in urls:
                    emails = Export_Emails.extract_emails(url)

                    if emails:
                        Export_Emails.save_emails_to_file(url, emails, directory, emails_file)
                        successful_urls.append(url)
                    else:
                        failed_urls.append(url)

                with open(scanned_websites_file, 'a') as file:
                    for url in successful_urls:
                        file.write(url + '\n')
                # if failed_urls:
                Export_Emails.save_failed_urls(failed_urls, directory, failed_urls_file)

                open(websites_file, 'w').close()
                print(f"{Fore.GREEN}Process completed. Scanned websites saved, failed URLs recorded, and websites.txt cleared.")
        except KeyboardInterrupt:
            pass
        finally:
            print(f"{Fore.YELLOW}\nPress Space to go back to the menu")
            key = ke.get_key()
            ke.clear_screen()
            while key == ord(' '):
                pass
            return