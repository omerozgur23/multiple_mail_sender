from tabulate import tabulate
from app_title import print_title
from colorama import Fore, Style, init
from key_event import Key_Event as ke

init(autoreset=True)

class Table:
    def draw_table(company_emails):
        ke.clear_screen()
        print_title()
        print(f"\n{Fore.GREEN}{'='*35}")
        print(f"\n{Fore.GREEN}{Style.BRIGHT}E-Mail addresses to be sent:")
        print(f"\n{Fore.GREEN}{'='*35}")

        table = [[i+1, company_emails[i]] for i in range(len(company_emails))]
        print(tabulate(table, headers=["No", "E-Mail Address"], tablefmt="fancy_grid"))