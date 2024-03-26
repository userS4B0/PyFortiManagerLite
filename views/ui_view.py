# File: /views/ui_view.py

import os

# Constants
VERSION = "0.2"
URL = "https://github.com/userS4B0/PyFortiManagerLite"

PAYLOADS = {
    "1": "single-backup",
    "2": "multi-backup",
    "3": "sync-objects",
    "4": "scrape-data",
}


class UIView:
    """View class responsible for user interface."""

    @staticmethod
    def print_banner():
        """Prints the program banner."""
        banner = f"""
        # {'=' * 129} #
        # {'By: UserS4B0'.center(127)} #
        # {f'({URL})'.center(127)} #
        # {'=' * 129} #
        """
        print(banner)

    @staticmethod
    def print_menu():
        """Prints the main menu options."""
        print("Menu:")
        for idx, option in enumerate(UIView.get_menu_options(), start=1):
            print(f"{idx}. {option}")

    @staticmethod
    def print_payloads_menu():
        """Prints the payloads menu options."""
        print("Payloads menu: ")
        for idx, payload in PAYLOADS.items():
            print(f"{idx}. {payload}")
        print("5. Go back")
        print("6. Exit")

    @staticmethod
    def clear_terminal():
        """Clears the terminal screen."""
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def print_separator(length):
        """Prints a separator line of specified length."""
        print("=" * length)

    @staticmethod
    def pause_flow():
        """Pauses the program flow until any key is pressed."""
        input("Press ANY KEY to continue.")

    @staticmethod
    def get_menu_options():
        """Returns a list of main menu options."""
        return [
            "Show inventory",
            "Check inventory connectivity",
            "Execute payload",
            "Settings",
            "Exit program",
        ]
