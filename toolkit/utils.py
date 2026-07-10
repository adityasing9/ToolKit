class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def init():
        import os
        if os.name == 'nt':
            os.system('color') # Enables ANSI escape codes in Windows cmd
