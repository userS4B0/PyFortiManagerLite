import os

VERSION = '0.2'
URL = 'https://github.com/userS4B0/PyFortiManagerLite'

PAYLOADS = {
    "1": "single-backup",
    "2": "multi-backup",
    "3": "sync-objects",
    "4": "scrape-data"
}

def load_banner():

    banner = f"""
    #  ================================================================================================================================  #
    #  __________       ___________               __   __   _____                                              ___     __  __            #
    #  \\______   \\___ __\\_   _____/ ____ ________/  |_|__| /     \\ _____    ____ _____     ____   ____ _______|   |   |__|/  |_  ____    #
    #   |     ___/   |  | |  ___)  / __ \\\\_  __ \\   __\\  |/  \\ /  \\\\__  \\  /    \\\\__  \\   / ___\\_/ __ \\\\_  __ \\   |   |  |   __\\/ __ \\   #
    #   |    |    \\___  | |  \\__  (  \\_\\ )|  | \\/|  | |  |    \\    \\/ __ \\_   |  \\/ __ \\_/ /_/  \\  ___/_|  | \\/   |___|  ||  | \\  ___/_  #
    #   |____|    / ____|/___  /   \\____/ |__|   |__| |__|____/\\_  /____  /___|  /____  /\\___  / \\___  /|__|  |______ \\__||__|  \\___  /  #
    #             \\/         \\/                                  \\/     \\/     \\/     \\//_____/      \\/              \\/             \\/   #
    #                                                                                                                                    #
    #                                                                                                                                    #
    #                                                                                                                                    #
    #                                                               By: UserS4B0 ({URL})  v{VERSION}  #
    #                                                                                                                                    #
    #  ================================================================================================================================  #
    """

    print(banner)

def load_main_menu():
    print("Menu:")
    print("1. Show inventory")
    print("2. Check inventory conectivity")
    print("3. Execute payload")
    print("4. Settings")
    print("5. Exit program")
    return input("Choose an option: ")

def load_payloads_menu():
    print("Payloads menu: ")
    for payload in PAYLOADS.keys():
        print(f"{payload}: {PAYLOADS[payload]}")
    print("5. Go back")
    print("6. Exit")

    return input("Choose a payload: ")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def separator(length):
    print("=" * length)