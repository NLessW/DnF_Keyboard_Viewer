import tkinter as tk
from pynput import keyboard

class KeyboardViewer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("키보드 뷰어")
        self.current_mode = "light"
        self.current_background = "#f0f0f0"
        self.buttons = {}
        self.create_ui()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def create_ui(self):
        self.main_frame = tk.Frame(self.window, bg=self.current_background)
        self.main_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.arrow_frame = tk.Frame(self.window, bg=self.current_background)
        self.arrow_frame.pack(side=tk.LEFT, padx=10, pady=10)

        keys = ['q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'f', 'g', 'h', 'ctrl', 'alt', 'up', 'left', 'down', 'right', 'z', 'x', 'c']

        for i in range(3):
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(7):
            self.main_frame.grid_columnconfigure(i, weight=1)

        button_color = "white"
        text_color = "black"

        # QWERTY
        for i, key in enumerate(['q', 'w', 'e', 'r', 't', 'y']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, bg=button_color, fg=text_color)
            self.buttons[key].grid(row=0, column=i, padx=2, pady=2)

        # CTRL
        self.buttons['ctrl'] = tk.Button(self.main_frame, text='CTRL', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['ctrl'].grid(row=0, column=6, padx=2, pady=2)

        # ASDFGH
        for i, key in enumerate(['a', 's', 'd', 'f', 'g', 'h']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, bg=button_color, fg=text_color)
            self.buttons[key].grid(row=1, column=i, padx=2, pady=2)

        # ALT
        self.buttons['alt'] = tk.Button(self.main_frame, text='ALT', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['alt'].grid(row=1, column=6, padx=2, pady=2)

        # ZXC
        for i, key in enumerate(['z', 'x', 'c']):
            self.buttons[key] = tk.Button(self.main_frame, text=key.upper(), width=6, height=2, bg=button_color, fg=text_color)
            self.buttons[key].grid(row=2, column=i, padx=2, pady=2)

        # Arrow keys
        self.buttons['up'] = tk.Button(self.arrow_frame, text='↑', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['up'].grid(row=0, column=1, padx=2, pady=2)

        self.buttons['left'] = tk.Button(self.arrow_frame, text='←', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['left'].grid(row=1, column=0, padx=2, pady=2)

        self.buttons['down'] = tk.Button(self.arrow_frame, text='↓', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['down'].grid(row=1, column=1, padx=2, pady=2)

        self.buttons['right'] = tk.Button(self.arrow_frame, text='→', width=6, height=2, bg=button_color, fg=text_color)
        self.buttons['right'].grid(row=1, column=2, padx=2, pady=2)

        # Double-click event binding
        self.window.bind('<Double-1>', lambda e: self.open_settings())

    def on_press(self, key):
        k = self.normalize_key(key)
        if k in self.buttons:
            self.buttons[k].config(bg=self.get_active_color())

    def on_release(self, key):
        k = self.normalize_key(key)
        if k in self.buttons:
            self.buttons[k].config(bg=self.get_inactive_color())

    def normalize_key(self, key):
        k = str(key).replace("'", "")
        if k in ["Key.ctrl_l", "Key.ctrl_r"]:
            return "ctrl"
        elif k in ["Key.alt_l", "Key.alt_r"]:
            return "alt"
        elif k.startswith("Key."):
            return k[4:]
        return k

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

    def open_settings(self):
        settings_window = tk.Toplevel(self.window)
        settings_window.title("설정")
        settings_window.geometry("200x100")

        # 배경색 변경 버튼
        bg_button = tk.Button(settings_window, text="배경색 변경", width=15, 
                              command=self.open_color_settings)
        bg_button.pack(pady=10)

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
        self.current_background = color
        self.window.configure(bg=color)
        self.main_frame.configure(bg=color)
        self.arrow_frame.configure(bg=color)

        if mode == "light":
            self.current_mode = "light"
            button_color = "white"
            text_color = "black"
        elif mode == "dark":
            self.current_mode = "dark"
            button_color = "#333333"
            text_color = "white"
        elif mode == "chroma":
            return

        for button in self.buttons.values():
            button.configure(bg=button_color, fg=text_color)
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    viewer = KeyboardViewer()
    viewer.run()
