import os
import sys
# Platform-specific imports
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix-like
    import tty
    import termios
    import select

class Key_Event:
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def move_cursor(y, x):
        print(f"\033[{y};{x}H", end='')

    def save_cursor():
        print("\033[s", end='')

    def restore_cursor():
        print("\033[u", end='')

    def hide_cursor():
        print("\033[?25l", end='', flush=True)

    def show_cursor():
        print("\033[?25h", end='', flush=True)

    def get_key():
        if os.name == 'nt':  # Windows
            key = msvcrt.getch()
            if key == b'\xe0':  # Special key (like arrows)
                key = msvcrt.getch()
                return {b'H': 'up', b'P': 'down'}.get(key, 'other')
            return key.decode('utf-8')
        else:  # Unix-like
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch += sys.stdin.read(2)
                    if ch == '\x1b[A':
                        return 'up'
                    elif ch == '\x1b[B':
                        return 'down'
                    elif ch == '\x1b[C':
                        return 'right'
                    elif ch == '\x1b[D':
                        return 'left'
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)