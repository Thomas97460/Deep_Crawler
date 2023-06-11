import shutil

def center_text(text):
    terminal_width = shutil.get_terminal_size().columns
    text_width = len(text)
    padding_width = (terminal_width - text_width) // 2
    centered_text = ' ' * padding_width + text + ' ' * padding_width
    return centered_text

def title(title):
    terminal_width = shutil.get_terminal_size().columns
    horizontal_line = ('-' * (terminal_width//2 - len(title)//2 - 2))
    final = horizontal_line + " " + title + " " + horizontal_line
    return final

def error(error) :
    RED = "\033[91m"
    RESET = "\033[0m"
    terminal_width = shutil.get_terminal_size().columns
    horizontal_line = ('-' * (terminal_width//2 - len(error)//2 - 2))
    final = horizontal_line + " " + RED + error + RESET + " " + horizontal_line
    return final

def blue(text) :
    BLUE = "\033[94m"
    RESET = "\033[0m"
    return BLUE + text + RESET

def green(text) :
    GREEN = "\033[92m"
    RESET = "\033[0m"
    return GREEN + text + RESET

def yellow(text) :
    GREEN = "\033[33m"
    RESET = "\033[0m"
    return GREEN + text + RESET

def red(text) :
    RED = "\033[91m"
    RESET = "\033[0m"
    return RED + text + RESET