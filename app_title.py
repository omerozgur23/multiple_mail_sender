from colorama import Fore, Style, init

init(autoreset=True)

def print_title():
    print(f"{Fore.YELLOW}Press Ctrl+C to exit at any time.{Style.RESET_ALL}")
    title = r"""
  __  __           _   _     ____                       _               
 |  \/  |   __ _  (_) | |   / ___|    ___   _ __     __| |   ___   _ __ 
 | |\/| |  / _` | | | | |   \___ \   / _ \ | '_ \   / _` |  / _ \ | '__|
 | |  | | | (_| | | | | |    ___) | |  __/ | | | | | (_| | |  __/ | |   
 |_|  |_|  \__,_| |_| |_|   |____/   \___| |_| |_|  \__,_|  \___| |_|   

    """
    print(Fore.GREEN + Style.NORMAL + title)