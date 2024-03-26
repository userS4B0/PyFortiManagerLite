import os

def pause_flow(): input("Press ANY KEY to continue...")
def clear_terminal(): os.system('cls' if os.name == 'nt' else 'clear')
def separator(length): return("=" * length)