import tkinter as tk
from tkinter import messagebox
from RequestHandler import handle, Result

WINDOW_SIZE = 480


class Console:
    def __init__(self, root):
        self.root = root
        self.console = tk.Text(root, state=tk.DISABLED, height=int(WINDOW_SIZE/15), width=int(WINDOW_SIZE/7.1))
        self.console.pack(side=tk.LEFT, padx=5, pady=5)
        self.console.configure(wrap=tk.NONE)

    def clear(self):
        self.console.configure(state="normal")
        self.console.delete("1.0", tk.END)
        self.console.configure(state="disabled")
        self.root.update_idletasks()

    def writer(self, txt):
        self.console.configure(state="normal")
        self.console.insert(tk.INSERT, f"{txt}\n")
        self.console.configure(state="disabled")
        self.root.update_idletasks()


def init_gui():
    # Init GUI
    root = tk.Tk()
    root.geometry(f"{2*WINDOW_SIZE}x{WINDOW_SIZE}")
    root.title("my_task")

    # Add text field
    label = tk.Label(root, text="Number of addresses:")
    label.pack(padx=5, pady=5)

    # Handle Return keypress
    def on_enter_handler(event):
        if event.state == 0 and event.keysym == "Return":
            start_handler()

    # Parameter entry field
    entry = tk.Entry(root)
    entry.bind("<KeyPress>", on_enter_handler)
    entry.pack()

    # Handle start event
    def start_handler():
        # Check if handler is already running
        if start_button["state"] == tk.DISABLED:
            return
        start_button.configure(state="disabled")

        console.clear()
        display.clear()
        
        result, message = handle(entry.get(), console.writer)
        if result in [Result.RETRY, Result.FATAL]:
            messagebox.showerror(title="Error", message=message)
            if result == Result.FATAL:
                exit(1)
        else:
            for line in message:
                display.writer(line)

        start_button.configure(state="normal")

    # Start Button
    start_button = tk.Button(root, text="Start", command=start_handler)
    start_button.pack(padx=5, pady=5)

    # Text areas
    console = Console(root)
    display = Console(root)

    return root


if __name__ == "__main__":
    root = init_gui()
    root.mainloop()
