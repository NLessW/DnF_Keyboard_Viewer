import tkinter as tk
from tkinter import simpledialog
from pynput import keyboard

class KeyboardLayout:
    def __init__(self):
        self.key_mappings = {}
        self.reverse_mappings = {}
        self.original_keys = ['q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h', 'ctrl', 'alt', 'z', 'x', 'c', 'space', 'caps_lock', 'up', 'down', 'left', 'right']
        self.active_keys = self.original_keys.copy()

    def change_key(self, key, new_key):
        if new_key and new_key != key:
            if key in self.key_mappings:
                old_mapping = self.key_mappings[key]
                if old_mapping in self.reverse_mappings:
                    del self.reverse_mappings[old_mapping]
            self.key_mappings[key] = new_key
            self.reverse_mappings[new_key] = key
            if new_key not in self.active_keys:
                self.active_keys.append(new_key)
            if key in self.active_keys:
                self.active_keys.remove(key)

    def reset_mappings(self):
        self.key_mappings.clear()
        self.reverse_mappings.clear()
        self.active_keys = self.original_keys.copy()

class ThemeManager:
    def __init__(self):
        self.current_mode = "light"
        self.current_background = "#f0f0f0"

    def get_active_color(self):
        return {
            "light": "red",
            "dark": "#ff6666",
            "chroma": "red" if self.current_mode == "light" else "#ff6666"
        }.get(self.current_mode, "red")

    def get_inactive_color(self):
        return {
            "light": "white",
            "dark": "#333333",
            "chroma": "white" if self.current_mode == "light" else "#333333"
        }.get(self.current_mode, "white")

    def change_mode(self, color, mode):
        self.current_background = color
        self.current_mode = mode

class KeyboardViewer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("키보드 뷰어")
        self.layout = KeyboardLayout()
        self.theme = ThemeManager()
        self.buttons = {}
        self.create_ui()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.changing_key = False
        self.key_to_change = None

    def create_ui(self):
        self.main_frame = tk.Frame(self.window, bg=self.theme.current_background)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.arrow_frame = tk.Frame(self.window, bg=self.theme.current_background)
        self.arrow_frame.pack(side=tk.LEFT, padx=10, pady=10)

        for i in range(3):
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(7):
            self.main_frame.grid_columnconfigure(i, weight=1)

        button_color = "white"
        text_color = "black"

        for i, key in enumerate(['q', 'w', 'e', 'r', 't', 'y']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, 
                                          bg=button_color, fg=text_color, command=lambda k=key: self.start_change_key(k))
            self.buttons[key].grid(row=0, column=i, padx=2, pady=2)

        self.buttons['ctrl'] = tk.Button(self.main_frame, text='CTRL', width=6, height=2, 
                                         bg=button_color, fg=text_color, command=lambda k='ctrl': self.start_change_key(k))
        self.buttons['ctrl'].grid(row=0, column=6, padx=2, pady=2)

        for i, key in enumerate(['a', 's', 'd', 'f', 'g', 'h']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, 
                                          bg=button_color, fg=text_color, command=lambda k=key: self.start_change_key(k))
            self.buttons[key].grid(row=1, column=i, padx=2, pady=2)

        self.buttons['alt'] = tk.Button(self.main_frame, text='ALT', width=6, height=2, 
                                        bg=button_color, fg=text_color, command=lambda k='alt': self.start_change_key(k))
        self.buttons['alt'].grid(row=1, column=6, padx=2, pady=2)

        for i, key in enumerate(['z', 'x', 'c']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, 
                                          bg=button_color, fg=text_color, command=lambda k=key: self.start_change_key(k))
            self.buttons[key].grid(row=2, column=i, padx=2, pady=2)

        self.buttons['space'] = tk.Button(self.main_frame, text='SPACE', width=22, height=2,
                                          bg=button_color, fg=text_color, command=lambda k='space': self.start_change_key(k))
        self.buttons['space'].grid(row=2, column=3, columnspan=3, padx=2, pady=2)

        self.buttons['caps_lock'] = tk.Button(self.main_frame, text='CAPS', width=6, height=2,
                                              bg=button_color, fg=text_color, command=lambda k='caps_lock': self.start_change_key(k))
        self.buttons['caps_lock'].grid(row=2, column=6, padx=2, pady=2)

        arrow_keys = ['up', 'left', 'down', 'right']
        arrow_symbols = ['↑', '←', '↓', '→']
        for key, symbol in zip(arrow_keys, arrow_symbols):
            self.buttons[key] = tk.Button(self.arrow_frame, text=symbol, width=6, height=2, 
                                        bg=button_color, fg=text_color, 
                                        command=lambda k=key: self.start_change_key(k))
            row = 0 if key == 'up' else 1
            col = 1 if key in ['up', 'down'] else (0 if key == 'left' else 2)
            self.buttons[key].grid(row=row, column=col, padx=2, pady=2)

        self.window.bind('<Double-1>', lambda e: self.open_settings())

    def start_change_key(self, key):
        self.changing_key = True
        self.key_to_change = key
        self.buttons[key].config(text="Press any key")

    def change_key(self, key, new_key):
        self.layout.change_key(key, new_key)
        if new_key:
            self.buttons[key].config(text=f"{new_key.upper()}")

    def reset_mappings(self):
        self.layout.reset_mappings()
        for key in self.layout.original_keys:
            if key == 'space':
                self.buttons[key].config(text='SPACE')
            elif key == 'caps_lock':
                self.buttons[key].config(text='CAPS')
            else:
                self.buttons[key].config(text=key.upper())

    def on_press(self, key):
        k = self.normalize_key(key)
        if self.changing_key:
            self.change_key(self.key_to_change, k)
            self.changing_key = False
            self.key_to_change = None
            return

        if k in self.layout.reverse_mappings:
            original_key = self.layout.reverse_mappings[k]
            self.buttons[original_key].config(bg=self.theme.get_active_color())
        elif k in self.buttons and k in self.layout.active_keys:
            self.buttons[k].config(bg=self.theme.get_active_color())

    def on_release(self, key):
        k = self.normalize_key(key)
        if k in self.layout.reverse_mappings:
            original_key = self.layout.reverse_mappings[k]
            self.buttons[original_key].config(bg=self.theme.get_inactive_color())
        elif k in self.buttons and k in self.layout.active_keys:
            self.buttons[k].config(bg=self.theme.get_inactive_color())

    def normalize_key(self, key):
        if isinstance(key, keyboard.KeyCode):
            return key.char if key.char else f'special_{key.vk}'
        elif isinstance(key, keyboard.Key):
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                return 'ctrl'
            elif key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
                return 'alt'
            elif key == keyboard.Key.up:
                return 'up'
            elif key == keyboard.Key.down:
                return 'down'
            elif key == keyboard.Key.left:
                return 'left'
            elif key == keyboard.Key.right:
                return 'right'
            return key.name
        return str(key)

    def open_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("설정")
        settings_window.geometry("200x150")

        bg_button = tk.Button(settings_window, text="배경색 변경", width=15, 
                              command=self.open_color_settings)
        bg_button.pack(pady=10)

        reset_button = tk.Button(settings_window, text="키 매핑 초기화", width=15,
                                 command=self.reset_mappings)
        reset_button.pack(pady=10)

    def open_color_settings(self):
        color_window = tk.Toplevel(self.window)
        color_window.title("배경색 설정")
        color_window.geometry("200x150")

        colors = [("Light Mode", "white", "light"), 
                  ("Dark Mode", "#1e1e1e", "dark"), 
                  ("Chroma Mode", "#00ff00", "chroma")]
        
        for text, color, mode in colors:
            button = tk.Button(color_window, text=text, width=15, 
                               command=lambda c=color, m=mode: self.change_mode(c, m))
            button.pack(pady=5)

    def change_mode(self, color, mode):
        self.theme.change_mode(color, mode)
        self.window.configure(bg=color)
        self.main_frame.configure(bg=color)
        self.arrow_frame.configure(bg=color)

        if mode in ["light", "dark"]:
            button_color = "white" if mode == "light" else "#333333"
            text_color = "black" if mode == "light" else "white"
            for button in self.buttons.values():
                button.configure(bg=button_color, fg=text_color)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    viewer = KeyboardViewer()
    viewer.run()
